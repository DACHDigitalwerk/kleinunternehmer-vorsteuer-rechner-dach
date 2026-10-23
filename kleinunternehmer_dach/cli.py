# -*- coding: utf-8 -*-
"""
Kommandozeilenwerkzeug (CLI) 'dach-kleinunternehmer':
Schwellenwertprüfungen & Vorsteuer-Rentabilitätsanalysen für DE, AT und CH.
"""

import sys
import argparse
import json
from .calculator import check_threshold, calculate_profitability, calculate_break_even
from .models import ProfitabilityInput
from .rates import COUNTRY_RATES_2026


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dach-kleinunternehmer",
        description="DACH Kleinunternehmer- & USt-Vorsteuer-Rechner 2026 (EU-Richtlinie DE, AT, CH)",
        epilog="Entwickelt von DACH Digitalwerk. Web-Tool: https://dach-digitalwerk.netlify.app/kleinunternehmer-vorsteuer-rechner/"
    )
    parser.add_argument("--version", action="version", version="dach-kleinunternehmer 1.0.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Verfügbare Befehle")

    # 1. check-threshold
    p_check = subparsers.add_parser("check", help="Prüft Vorjahres- & Planumsatz gegen amtliche Schwellenwerte 2026")
    p_check.add_argument("--country", "-c", choices=["DE", "AT", "CH"], default="DE", help="Ländercode (DE, AT, CH)")
    p_check.add_argument("--prev", "-p", type=float, required=True, help="Umsatz des vorangegangenen Kalenderjahres")
    p_check.add_argument("--curr", "-u", type=float, required=True, help="Voraussichtlicher Umsatz im laufenden Kalenderjahr")
    p_check.add_argument("--nonprofit", action="store_true", help="Gilt für gemeinnützige Sport-/Kulturvereine (CH: 150.000 CHF Schwelle)")
    p_check.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    # 2. compare-profitability
    p_comp = subparsers.add_parser("compare", help="Rentabilitätsvergleich: Kleinunternehmer vs. Regelbesteuerung")
    p_comp.add_argument("--country", "-c", choices=["DE", "AT", "CH"], default="DE", help="Ländercode (DE, AT, CH)")
    p_comp.add_argument("--revenue", "-r", type=float, required=True, help="Geplanter Jahresumsatz (EUR / CHF)")
    p_comp.add_argument("--b2b", "-b", type=float, default=30.0, help="Anteil B2B-Kunden in Prozent (0 - 100)")
    p_comp.add_argument("--expenses", "-e", type=float, default=0.0, help="Laufende jährliche Betriebsausgaben (Netto)")
    p_comp.add_argument("--investments", "-i", type=float, default=0.0, help="Geplante Investitionen / Anschaffungen (Netto)")
    p_comp.add_argument("--input-tax", type=float, default=None, help="Eingangssteuersatz z.B. 0.19 für 19%%")
    p_comp.add_argument("--output-tax", type=float, default=None, help="Ausgangssteuersatz z.B. 0.19 für 19%%")
    p_comp.add_argument("--admin-cost", type=float, default=400.0, help="Verwaltungsmehrkosten Regelbesteuerung (Standard: 400 €)")
    p_comp.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    # 3. break-even
    p_be = subparsers.add_parser("break-even", help="Ermittelt Break-Even-Punkte für Investitionen & B2B-Anteil")
    p_be.add_argument("--country", "-c", choices=["DE", "AT", "CH"], default="DE", help="Ländercode")
    p_be.add_argument("--revenue", "-r", type=float, required=True, help="Geplanter Jahresumsatz")
    p_be.add_argument("--b2b", "-b", type=float, default=30.0, help="B2B-Anteil in Prozent")
    p_be.add_argument("--expenses", "-e", type=float, default=0.0, help="Laufende Betriebsausgaben Netto")
    p_be.add_argument("--admin-cost", type=float, default=400.0, help="Verwaltungsmehrkosten")
    p_be.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    return parser


def format_currency(val: float, sym: str) -> str:
    return f"{val:,.2f} {sym}".replace(",", "X").replace(".", ",").replace("X", ".")


def run_cli(args=None):
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        sys.exit(0)

    try:
        if parsed.command == "check":
            res = check_threshold(
                country=parsed.country,
                prev_year_turnover=parsed.prev,
                current_year_turnover=parsed.curr,
                is_nonprofit=getattr(parsed, "nonprofit", False)
            )

            if parsed.json:
                print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
                return

            print("=" * 68)
            print(f"📊 DACH KLEINUNTERNEHMER SCHWELLENWERT-CHECK 2026 [{res.country}]")
            print("=" * 68)
            print(f"Land:                  {res.country_name}")
            print(f"Vorjahresumsatz:       {format_currency(res.prev_year_turnover, res.currency_symbol)}")
            print(f"Laufendes Jahr:        {format_currency(res.current_year_turnover, res.currency_symbol)}")
            print(f"Amtliche Grenze 2026:  {format_currency(res.threshold_limit, res.currency_symbol)}")
            print(f"Auslastung der Grenze: {res.utilization_pct:.1f} %")
            print(f"Status:                [{res.threshold_status}]")
            print(f"Berechtigung:          {'✅ ZULÄSSIG' if res.is_eligible else '❌ AUSGESCHLOSSEN / WEGFALL'}")
            print("-" * 68)
            print(f"Befund:\n{res.message}")
            if res.action_recommendations:
                print("\nHandlungsempfehlungen:")
                for a in res.action_recommendations:
                    print(f"  • {a}")
            print("=" * 68)

        elif parsed.command == "compare":
            params = ProfitabilityInput(
                country=parsed.country,
                planned_revenue=parsed.revenue,
                b2b_share_pct=parsed.b2b,
                expenses_operating=parsed.expenses,
                investments=parsed.investments,
                input_tax_rate=parsed.input_tax,
                output_tax_rate=parsed.output_tax,
                admin_cost_standard_tax=parsed.admin_cost,
            )
            res = calculate_profitability(params)

            if parsed.json:
                print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
                return

            sym = res.currency_symbol
            print("=" * 72)
            print(f"⚖️  KLEINUNTERNEHMER vs. REGELBESTEUERUNG: RENTABILITÄT 2026 [{res.country}]")
            print("=" * 72)
            print(f"Geplanter Gesamtumsatz:        {format_currency(res.planned_revenue, sym)}")
            print(f"  ├─ B2C-Umsatz ({res.b2c_share_pct:.0f} %):         {format_currency(res.b2c_revenue, sym)}")
            print(f"  └─ B2B-Umsatz ({res.b2b_share_pct:.0f} %):         {format_currency(res.b2b_revenue, sym)}")
            print(f"Betriebsausgaben & Investition: {format_currency(res.total_expenses_net, sym)} Netto")
            print("-" * 72)
            print(f"1. USt-Ersparnis bei B2C:      +{format_currency(res.output_tax_b2c, sym)} (Kleinunternehmer-Vorteil)")
            print(f"2. Bürokratie-Ersparnis:       +{format_currency(res.admin_cost_diff, sym)} (USt-Voranmeldungen)")
            print(f"3. Entgangener Vorsteuerabzug: -{format_currency(res.input_tax_deductible, sym)} (Nachteil auf Ausgaben)")
            print("-" * 72)
            adv = res.net_advantage_kleinunternehmer
            adv_str = f"+{format_currency(adv, sym)}" if adv >= 0 else f"-{format_currency(abs(adv), sym)}"
            print(f"NETTO-VORTEIL KLEINUNTERNEHMER: {adv_str} / Jahr")
            print(f"EMPFEHLUNG:                    [{res.recommendation}] -> {res.recommendation_title}")
            print(f"\nDetails:\n{res.recommendation_text}")
            print("\nBegründungspunkte:")
            for r in res.summary_reasons:
                print(f"  ✓ {r}")
            print("-" * 72)
            print(f"Break-Even Investitionshöhe:   {format_currency(res.break_even_investments, sym)}")
            print(f"Break-Even B2B-Kundenanteil:   {res.break_even_b2b_share_pct:.1f} %")
            print("=" * 72)

        elif parsed.command == "break-even":
            params = ProfitabilityInput(
                country=parsed.country,
                planned_revenue=parsed.revenue,
                b2b_share_pct=parsed.b2b,
                expenses_operating=parsed.expenses,
                admin_cost_standard_tax=parsed.admin_cost,
            )
            res = calculate_break_even(params)
            if parsed.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return

            sym = COUNTRY_RATES_2026[parsed.country].CURRENCY_SYMBOL
            print("=" * 60)
            print(f"🎯 BREAK-EVEN-ANALYSE 2026 [{parsed.country}]")
            print("=" * 60)
            print(f"Investitionsschwelle (CAPEX): {format_currency(res['break_even_investments'], sym)}")
            print(f"B2B-Kundenanteilschwelle:     {res['break_even_b2b_share_pct']:.1f} %")
            print(f"Aktueller Netto-Vorteil:      {format_currency(res['current_net_advantage'], sym)}")
            print("=" * 60)

    except Exception as e:
        sys.stderr.write(f"Fehler: {e}\n")
        sys.exit(1)


def main():
    run_cli()


if __name__ == "__main__":
    main()
