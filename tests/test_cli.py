# -*- coding: utf-8 -*-
"""Unit-Tests für die CLI-Schnittstelle."""

import unittest
import io
import json
from contextlib import redirect_stdout
from kleinunternehmer_dach.cli import run_cli, build_parser


class TestCli(unittest.TestCase):
    def test_parser_setup(self):
        parser = build_parser()
        self.assertIsNotNone(parser)

    def test_cli_check_command_json(self):
        f = io.StringIO()
        with redirect_stdout(f):
            run_cli(["check", "--country", "DE", "--prev", "20000", "--curr", "24000", "--json"])
        output = f.getvalue()
        data = json.loads(output)
        self.assertEqual(data["country"], "DE")
        self.assertTrue(data["is_eligible"])
        self.assertEqual(data["threshold_status"], "WARNING_NEAR_LIMIT")

    def test_cli_compare_command_json(self):
        f = io.StringIO()
        with redirect_stdout(f):
            run_cli([
                "compare",
                "--country", "DE",
                "--revenue", "22000",
                "--b2b", "40",
                "--expenses", "3000",
                "--investments", "1000",
                "--json"
            ])
        output = f.getvalue()
        data = json.loads(output)
        self.assertEqual(data["country"], "DE")
        self.assertIn("net_advantage_kleinunternehmer", data)
        self.assertIn("recommendation", data)

    def test_cli_break_even_command_json(self):
        f = io.StringIO()
        with redirect_stdout(f):
            run_cli([
                "break-even",
                "--country", "AT",
                "--revenue", "30000",
                "--b2b", "50",
                "--expenses", "4000",
                "--json"
            ])
        output = f.getvalue()
        data = json.loads(output)
        self.assertIn("break_even_investments", data)
        self.assertIn("break_even_b2b_share_pct", data)

    def test_cli_check_human_output(self):
        f = io.StringIO()
        with redirect_stdout(f):
            run_cli(["check", "--country", "CH", "--prev", "50000", "--curr", "85000"])
        output = f.getvalue()
        self.assertIn("SCHWELLENWERT-CHECK 2026", output)
        self.assertIn("Schweiz", output)
        self.assertIn("100.000,00 CHF", output)


if __name__ == "__main__":
    unittest.main()
