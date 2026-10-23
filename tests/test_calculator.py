# -*- coding: utf-8 -*-
"""Unit-Tests für die Rentabilitätsberechnung und Vorsteueranalyse."""

import unittest
from kleinunternehmer_dach.calculator import (
    calculate_profitability,
    calculate_break_even,
)
from kleinunternehmer_dach.models import ProfitabilityInput


class TestCalculator(unittest.TestCase):
    def test_profitability_pure_b2c_low_expenses(self):
        # Bei 100% B2C und geringen Betriebsausgaben lohnt sich Kleinunternehmerregelung extrem
        p = ProfitabilityInput(
            country="DE",
            planned_revenue=20000.0,
            b2b_share_pct=0.0,  # 100% B2C
            expenses_operating=1000.0,
            investments=0.0,
            admin_cost_standard_tax=400.0,
        )
        res = calculate_profitability(p)
        self.assertEqual(res.recommendation, "KLEINUNTERNEHMER")
        self.assertEqual(res.badge_color, "green")
        self.assertGreater(res.net_advantage_kleinunternehmer, 1000.0)
        # B2C USt = 20000 * (0.19 / 1.19) ~ 3193.28 €
        # Admin saved = 400 €
        # Vorsteuer entgangen = 1000 * 0.19 = 190 €
        # Netto-Vorteil ca. 3193.28 + 400 - 190 = 3403.28 €
        self.assertAlmostEqual(res.net_advantage_kleinunternehmer, 3403.28, delta=1.0)

    def test_profitability_pure_b2b_high_investments(self):
        # Bei 100% B2B und hohen Investitionen ist Regelbesteuerung viel günstiger
        p = ProfitabilityInput(
            country="DE",
            planned_revenue=22000.0,
            b2b_share_pct=100.0,  # 0% B2C
            expenses_operating=4000.0,
            investments=10000.0,  # 14.000 € Ausgaben
            admin_cost_standard_tax=300.0,
        )
        res = calculate_profitability(p)
        self.assertEqual(res.recommendation, "REGELBESTEUERUNG")
        self.assertEqual(res.badge_color, "blue")
        # Vorsteuer = 14000 * 0.19 = 2660 €
        # B2C Vorteil = 0
        # Admin saved = 300 €
        # Net advantage = 0 + 300 - 2660 = -2360 €
        self.assertEqual(res.net_advantage_kleinunternehmer, -2360.0)

    def test_break_even_investments(self):
        p = ProfitabilityInput(
            country="DE",
            planned_revenue=20000.0,
            b2b_share_pct=40.0,  # 60% B2C -> 12000 € B2C
            expenses_operating=2000.0,
            investments=0.0,
            admin_cost_standard_tax=400.0,
        )
        res = calculate_profitability(p)
        self.assertGreater(res.break_even_investments, 0.0)
        # Wenn wir genau die break_even_investments einsetzen, sollte net_advantage nahe 0 sein
        p_be = ProfitabilityInput(
            country="DE",
            planned_revenue=20000.0,
            b2b_share_pct=40.0,
            expenses_operating=2000.0,
            investments=res.break_even_investments,
            admin_cost_standard_tax=400.0,
        )
        res_be = calculate_profitability(p_be)
        self.assertAlmostEqual(res_be.net_advantage_kleinunternehmer, 0.0, delta=1.0)

    def test_austria_profitability(self):
        p = ProfitabilityInput(
            country="AT",
            planned_revenue=35000.0,
            b2b_share_pct=50.0,
            expenses_operating=5000.0,
            investments=1000.0,
        )
        res = calculate_profitability(p)
        self.assertEqual(res.country, "AT")
        self.assertEqual(res.currency, "EUR")
        self.assertEqual(res.input_tax_rate, 0.20)

    def test_switzerland_profitability(self):
        p = ProfitabilityInput(
            country="CH",
            planned_revenue=80000.0,
            b2b_share_pct=80.0,
            expenses_operating=15000.0,
            investments=5000.0,
        )
        res = calculate_profitability(p)
        self.assertEqual(res.country, "CH")
        self.assertEqual(res.currency, "CHF")
        self.assertEqual(res.input_tax_rate, 0.081)

    def test_calculate_break_even_helper(self):
        p = ProfitabilityInput(country="DE", planned_revenue=20000.0, b2b_share_pct=50.0)
        be = calculate_break_even(p)
        self.assertIn("break_even_investments", be)
        self.assertIn("break_even_b2b_share_pct", be)
        self.assertIn("current_net_advantage", be)


if __name__ == "__main__":
    unittest.main()
