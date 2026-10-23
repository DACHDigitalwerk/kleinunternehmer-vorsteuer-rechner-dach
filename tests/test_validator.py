# -*- coding: utf-8 -*-
"""Unit-Tests für Eingabe-Validierung."""

import unittest
from kleinunternehmer_dach.validator import (
    validate_country,
    validate_threshold_input,
    validate_profitability_input,
)
from kleinunternehmer_dach.models import ProfitabilityInput


class TestValidator(unittest.TestCase):
    def test_validate_valid_countries(self):
        self.assertEqual(validate_country("de"), "DE")
        self.assertEqual(validate_country("AT"), "AT")
        self.assertEqual(validate_country(" ch "), "CH")

    def test_validate_invalid_country_raises(self):
        with self.assertRaises(ValueError):
            validate_country("FR")
        with self.assertRaises(ValueError):
            validate_country("")

    def test_validate_threshold_valid(self):
        c, prev, curr = validate_threshold_input("de", 15000, 22000.50)
        self.assertEqual(c, "DE")
        self.assertEqual(prev, 15000.0)
        self.assertEqual(curr, 22000.50)

    def test_validate_threshold_negative_raises(self):
        with self.assertRaises(ValueError):
            validate_threshold_input("DE", -100, 10000)
        with self.assertRaises(ValueError):
            validate_threshold_input("DE", 10000, -50)

    def test_validate_profitability_b2b_range(self):
        p_valid = ProfitabilityInput(country="DE", planned_revenue=20000, b2b_share_pct=100.0)
        res = validate_profitability_input(p_valid)
        self.assertEqual(res.b2b_share_pct, 100.0)

        p_invalid = ProfitabilityInput(country="DE", b2b_share_pct=105.0)
        with self.assertRaises(ValueError):
            validate_profitability_input(p_invalid)

        p_neg = ProfitabilityInput(country="DE", b2b_share_pct=-5.0)
        with self.assertRaises(ValueError):
            validate_profitability_input(p_neg)

    def test_validate_profitability_negative_expenses(self):
        p_neg_exp = ProfitabilityInput(country="DE", expenses_operating=-500)
        with self.assertRaises(ValueError):
            validate_profitability_input(p_neg_exp)


if __name__ == "__main__":
    unittest.main()
