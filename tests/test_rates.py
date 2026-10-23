# -*- coding: utf-8 -*-
"""Unit-Tests für gesetzliche Grenzwerte und Steuersätze 2026."""

import unittest
from kleinunternehmer_dach.rates import (
    COUNTRY_RATES_2026,
    GermanyRates,
    AustriaRates,
    SwitzerlandRates,
)


class TestRates(unittest.TestCase):
    def test_germany_rates_2026(self):
        de = GermanyRates
        self.assertEqual(de.COUNTRY, "DE")
        self.assertEqual(de.CURRENCY, "EUR")
        # 2026 Grenzwert auf 25.000 € angehoben (Wachstumschancengesetz / EU-RL)
        self.assertEqual(de.THRESHOLD_PREV_YEAR, 25000.0)
        self.assertEqual(de.THRESHOLD_CURRENT_YEAR_NATIONAL, 25000.0)
        self.assertEqual(de.THRESHOLD_EU_CROSSBORDER, 100000.0)
        self.assertEqual(de.VAT_STANDARD, 0.19)
        self.assertEqual(de.VAT_REDUCED, 0.07)

    def test_austria_rates_2026(self):
        at = AustriaRates
        self.assertEqual(at.COUNTRY, "AT")
        self.assertEqual(at.CURRENCY, "EUR")
        # 2026 Grenzwert auf 42.000 € angehoben
        self.assertEqual(at.THRESHOLD_STANDARD, 42000.0)
        self.assertEqual(at.THRESHOLD_TOLERANCE, 55000.0)
        self.assertEqual(at.VAT_STANDARD, 0.20)
        self.assertEqual(at.VAT_REDUCED_1, 0.10)

    def test_switzerland_rates_2026(self):
        ch = SwitzerlandRates
        self.assertEqual(ch.COUNTRY, "CH")
        self.assertEqual(ch.CURRENCY, "CHF")
        self.assertEqual(ch.THRESHOLD_STANDARD, 100000.0)
        self.assertEqual(ch.THRESHOLD_NONPROFIT, 150000.0)
        self.assertEqual(ch.VAT_STANDARD, 0.081)
        self.assertEqual(ch.VAT_SPECIAL_LODGING, 0.038)
        self.assertEqual(ch.VAT_REDUCED, 0.026)

    def test_country_dict_completeness(self):
        self.assertIn("DE", COUNTRY_RATES_2026)
        self.assertIn("AT", COUNTRY_RATES_2026)
        self.assertIn("CH", COUNTRY_RATES_2026)


if __name__ == "__main__":
    unittest.main()
