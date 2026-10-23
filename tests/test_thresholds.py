# -*- coding: utf-8 -*-
"""Unit-Tests für Schwellenwert-Logik DE, AT, CH 2026."""

import unittest
from kleinunternehmer_dach.calculator import check_threshold


class TestThresholds(unittest.TestCase):
    # Deutschland 2026: 25.000 € Vorjahresschwelle
    def test_germany_below_threshold(self):
        res = check_threshold("DE", prev_year_turnover=15000, current_year_turnover=18000)
        self.assertTrue(res.is_eligible)
        self.assertEqual(res.threshold_status, "SAFE")
        self.assertEqual(res.threshold_limit, 25000.0)

    def test_germany_near_limit_warning(self):
        # 80% von 25.000 € = 20.000 €
        res = check_threshold("DE", prev_year_turnover=18000, current_year_turnover=22500)
        self.assertTrue(res.is_eligible)
        self.assertEqual(res.threshold_status, "WARNING_NEAR_LIMIT")
        self.assertEqual(res.utilization_pct, 90.0)

    def test_germany_prev_year_exceeded(self):
        res = check_threshold("DE", prev_year_turnover=25001, current_year_turnover=15000)
        self.assertFalse(res.is_eligible)
        self.assertEqual(res.threshold_status, "EXCEEDED")

    def test_germany_current_year_exceeded(self):
        res = check_threshold("DE", prev_year_turnover=20000, current_year_turnover=27000)
        self.assertFalse(res.is_eligible)
        self.assertEqual(res.threshold_status, "EXCEEDED")

    # Österreich 2026: 42.000 € Schwelle & 55.000 € Toleranz
    def test_austria_safe(self):
        res = check_threshold("AT", prev_year_turnover=30000, current_year_turnover=32000)
        self.assertTrue(res.is_eligible)
        self.assertEqual(res.threshold_status, "SAFE")
        self.assertEqual(res.threshold_limit, 42000.0)

    def test_austria_tolerance_zone(self):
        # Zwischen 42.000 € und 55.000 € ist die 1x in 5 Jahren Toleranzzone
        res = check_threshold("AT", prev_year_turnover=38000, current_year_turnover=48000)
        self.assertTrue(res.is_eligible)
        self.assertEqual(res.threshold_status, "TOLERANCE_ZONE")

    def test_austria_tolerance_exceeded(self):
        res = check_threshold("AT", prev_year_turnover=38000, current_year_turnover=56000)
        self.assertFalse(res.is_eligible)
        self.assertEqual(res.threshold_status, "EXCEEDED")

    # Schweiz 2026: 100.000 CHF Schwelle / 150.000 CHF gemeinnützig
    def test_switzerland_standard_safe(self):
        res = check_threshold("CH", prev_year_turnover=60000, current_year_turnover=75000)
        self.assertTrue(res.is_eligible)
        self.assertEqual(res.threshold_status, "SAFE")
        self.assertEqual(res.threshold_limit, 100000.0)

    def test_switzerland_standard_exceeded(self):
        res = check_threshold("CH", prev_year_turnover=80000, current_year_turnover=105000)
        self.assertFalse(res.is_eligible)
        self.assertEqual(res.threshold_status, "EXCEEDED")

    def test_switzerland_nonprofit_limit(self):
        res = check_threshold("CH", prev_year_turnover=110000, current_year_turnover=130000, is_nonprofit=True)
        self.assertTrue(res.is_eligible)
        self.assertEqual(res.threshold_limit, 150000.0)
        self.assertEqual(res.threshold_status, "WARNING_NEAR_LIMIT")


if __name__ == "__main__":
    unittest.main()
