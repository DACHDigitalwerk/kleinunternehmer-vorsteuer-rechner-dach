# -*- coding: utf-8 -*-
"""
Berechnungskern für Schwellenwert-Monitoring und Vorsteuer-Rentabilität 2026.
DE (§ 19 UStG), AT (§ 6 Abs. 1 Z 27 UStG) und CH (Art. 10 MWSTG).
"""

from typing import Dict, Any, List
from .models import (
    ProfitabilityInput,
    ProfitabilityComparisonResult,
    ThresholdCheckResult,
)
from .rates import COUNTRY_RATES_2026, GermanyRates, AustriaRates, SwitzerlandRates
from .validator import validate_profitability_input, validate_threshold_input


def check_threshold(
    country: str,
    prev_year_turnover: float,
    current_year_turnover: float,
    is_nonprofit: bool = False
) -> ThresholdCheckResult:
    """
    Prüft Vorjahres- und Planumsatz gegen die amtlichen Grenzwerte 2026.
    """
    c, prev, curr = validate_threshold_input(country, prev_year_turnover, current_year_turnover)
    cfg = COUNTRY_RATES_2026[c]
    
    actions: List[str] = []
    notes: List[str] = []
    
    if c == "DE":
        limit = cfg.THRESHOLD_PREV_YEAR  # 25.000 € ab 2025/2026
        max_turnover = max(prev, curr)
        utilization = round((curr / limit) * 100.0, 1) if limit > 0 else 0.0
        
        notes.append(f"Gesetzliche Grundlage: {cfg.LEGAL_BASIS}")
        notes.append("Vorjahresschwelle: 25.000 € (Wachstumschancengesetz / EU-Kleinunternehmer-RL).")
        notes.append("Laufendes Kalenderjahr: Schwellenwert 25.000 € national bzw. 100.000 € EU-weit.")
        
        if prev > limit:
            is_eligible = False
            status = "EXCEEDED"
            msg = (
                f"Kleinunternehmerregelung 2026 ausgeschlossen: Der Vorjahresumsatz ({prev:,.2f} €) "
                f"übersteigt die gesetzliche Grenze von {limit:,.2f} € (§ 19 Abs. 1 UStG)."
            )
            actions.append("Regelbesteuerung anwenden: Umsatzsteuer in Rechnungen ausweisen (19 % bzw. 7 %).")
            actions.append("Monatliche/Vierteljährliche USt-Voranmeldungen (USt-VA) beim Finanzamt einreichen.")
            actions.append("Voller Vorsteuerabzug auf alle betrieblichen Eingangsrechnungen und Investitionen sichern.")
        elif curr > limit:
            is_eligible = False
            status = "EXCEEDED"
            msg = (
                f"Grenzübertritt im laufenden Jahr: Der prognostizierte Umsatz ({curr:,.2f} €) "
                f"übersteigt die Schwelle von {limit:,.2f} €. Die Befreiung entfällt mit Überschreitung."
            )
            actions.append("Rechnungsstellung rechtzeitig auf Ausweis der Umsatzsteuer umstellen.")
            actions.append("Finanzamt über den Wegfall der Kleinunternehmerregelung informieren.")
            actions.append("USt-IdNr. beantragen und Vorsteuer-Belege für das laufende Jahr sammeln.")
        elif curr >= limit * 0.80:
            is_eligible = True
            status = "WARNING_NEAR_LIMIT"
            msg = (
                f"Achtung, Schwellennähe: Ihr Umsatz ({curr:,.2f} €) erreicht {utilization:.1f} % der "
                f"25.000 €-Grenze. Puffer bis zum Grenzübertritt: {(limit - curr):,.2f} €."
            )
            actions.append("Monatliches Umsatz-Monitoring etablieren, um Nachzahlungen bei Überschreitung zu vermeiden.")
            actions.append("Rentabilitätsvergleich durchführen: Lohnt sich ein freiwilliger Wechsel zur Regelbesteuerung?")
        else:
            is_eligible = True
            status = "SAFE"
            msg = (
                f"Kleinunternehmerregelung uneingeschränkt anwendbar. Umsatz ({curr:,.2f} €) liegt "
                f"sicher unter der 25.000 €-Grenze (Auslastung: {utilization:.1f} %)."
            )
            actions.append("Rechnungen mit Hinweis auf § 19 UStG ohne Steuerausweis ausstellen.")
            actions.append("Keine monatlichen Voranmeldungen erforderlich (Bürokratieersparnis).")
            
        return ThresholdCheckResult(
            country="DE",
            country_name=cfg.NAME,
            currency=cfg.CURRENCY,
            currency_symbol=cfg.CURRENCY_SYMBOL,
            prev_year_turnover=prev,
            current_year_turnover=curr,
            is_eligible=is_eligible,
            threshold_limit=limit,
            threshold_status=status,
            utilization_pct=utilization,
            message=msg,
            statutory_basis=cfg.LEGAL_BASIS,
            action_recommendations=actions,
            legal_notes=notes,
        )

    elif c == "AT":
        limit = cfg.THRESHOLD_STANDARD  # 42.000 € ab 2025/2026
        tolerance = cfg.THRESHOLD_TOLERANCE  # 55.000 €
        utilization = round((curr / limit) * 100.0, 1) if limit > 0 else 0.0
        
        notes.append(f"Gesetzliche Grundlage: {cfg.LEGAL_BASIS}")
        notes.append("Schwellenwert 2026: 42.000 € Netto (angehoben von 35.000 € gem. EU-RL).")
        notes.append("Toleranzgrenze: Bis zu 55.000 € einmalig innerhalb von 5 Kalenderjahren zulässig.")
        
        if curr > tolerance:
            is_eligible = False
            status = "EXCEEDED"
            msg = (
                f"Toleranzgrenze überschritten ({curr:,.2f} € > {tolerance:,.2f} €). "
                f"Die unechte Steuerbefreiung entfällt zwingend."
            )
            actions.append("Sofortige Umstellung auf Regelbesteuerung mit 20 % / 10 % USt-Ausweis.")
            actions.append("Meldung an das zuständige Finanzamt Österreich.")
        elif curr > limit:
            is_eligible = True
            status = "TOLERANCE_ZONE"
            msg = (
                f"In der Toleranzzone ({curr:,.2f} €): Die Regelschwelle von {limit:,.2f} € ist überschritten, "
                f"liegt jedoch unter der 55.000 € Toleranzgrenze (§ 6 Abs. 1 Z 27 UStG)."
            )
            actions.append("Prüfen, ob die Toleranzregelung in den letzten 4 Wirtschaftsjahren bereits in Anspruch genommen wurde.")
            actions.append("Bei bereits verbrauchter Toleranz gilt rückwirkend die Regelbesteuerung.")
        elif curr >= limit * 0.80:
            is_eligible = True
            status = "WARNING_NEAR_LIMIT"
            msg = (
                f"Warnstufe Schwellennähe ({curr:,.2f} €): Sie erreichen {utilization:.1f} % der "
                f"42.000 € Basisgrenze."
            )
            actions.append("Umsatzströme überwachen und Vorsteuerabzugspotenzial kalkulieren.")
        else:
            is_eligible = True
            status = "SAFE"
            msg = (
                f"Österreichische Kleinunternehmerbefreiung sicher erfüllt ({curr:,.2f} € von 42.000 €)."
            )
            actions.append("Rechnungen mit Vermerk 'Umsatzsteuerfrei aufgrund der Kleinunternehmerregelung' versehen.")
            
        return ThresholdCheckResult(
            country="AT",
            country_name=cfg.NAME,
            currency=cfg.CURRENCY,
            currency_symbol=cfg.CURRENCY_SYMBOL,
            prev_year_turnover=prev,
            current_year_turnover=curr,
            is_eligible=is_eligible,
            threshold_limit=limit,
            threshold_status=status,
            utilization_pct=utilization,
            message=msg,
            statutory_basis=cfg.LEGAL_BASIS,
            action_recommendations=actions,
            legal_notes=notes,
        )

    else:  # CH
        limit = cfg.THRESHOLD_NONPROFIT if is_nonprofit else cfg.THRESHOLD_STANDARD
        utilization = round((curr / limit) * 100.0, 1) if limit > 0 else 0.0
        
        notes.append(f"Gesetzliche Grundlage: {cfg.LEGAL_BASIS}")
        notes.append(f"MWST-Befreiungsgrenze: {limit:,.2f} CHF Jahresumsatz weltweit aus steuerbaren Leistungen.")
        notes.append("MWST-Sätze 2026: 8,1 % Normalsatz, 3,8 % Beherbergung, 2,6 % reduzierter Satz.")
        notes.append("Option zur freiwilligen Unterstellung (Art. 10 Abs. 3 MWSTG) für Vorsteuerabzug.")
        
        if curr > limit:
            is_eligible = False
            status = "EXCEEDED"
            msg = (
                f"Obligatorische MWST-Pflicht in der Schweiz: Umsatz von {curr:,.2f} CHF "
                f"übersteigt die Befreiungsgrenze von {limit:,.2f} CHF (Art. 10 MWSTG)."
            )
            actions.append("Obligatorische Anmeldung bei der Eidgenössischen Steuerverwaltung (ESTV) innerhalb 30 Tagen.")
            actions.append("Wahl der Abrechnungsmethode: Effektive Methode (8,1 % + Vorsteuer) vs. Saldosteuersatz.")
        elif curr >= limit * 0.80:
            is_eligible = True
            status = "WARNING_NEAR_LIMIT"
            msg = (
                f"Achtung: Umsatz ({curr:,.2f} CHF) nähert sich der 100.000 CHF Schwelle ({utilization:.1f} %)."
            )
            actions.append("Rechtzeitige Vorbereitung der Buchhaltung auf MWST-Abrechnung (Art. 10 MWSTG).")
        else:
            is_eligible = True
            status = "SAFE"
            msg = (
                f"Von der MWST-Pflicht befreit. Umsatz ({curr:,.2f} CHF) liegt unter {limit:,.2f} CHF."
            )
            actions.append("Keine MWST auf Rechnungen ausweisen; keine ESTV-Quartalsabrechnungen nötig.")
            actions.append("Freiwillige Unterstellung prüfen, falls hohe Vorsteuern bei Investitionen anfallen.")
            
        return ThresholdCheckResult(
            country="CH",
            country_name=cfg.NAME,
            currency=cfg.CURRENCY,
            currency_symbol=cfg.CURRENCY_SYMBOL,
            prev_year_turnover=prev,
            current_year_turnover=curr,
            is_eligible=is_eligible,
            threshold_limit=limit,
            threshold_status=status,
            utilization_pct=utilization,
            message=msg,
            statutory_basis=cfg.LEGAL_BASIS,
            action_recommendations=actions,
            legal_notes=notes,
        )


def calculate_profitability(params: ProfitabilityInput) -> ProfitabilityComparisonResult:
    """
    Berechnet die wirtschaftliche Rentabilität: Kleinunternehmer vs. Regelbesteuerung.
    """
    p = validate_profitability_input(params)
    cfg = COUNTRY_RATES_2026[p.country]
    
    b2b_share = p.b2b_share_pct / 100.0
    b2c_share = 1.0 - b2b_share
    
    b2b_rev = round(p.planned_revenue * b2b_share, 2)
    b2c_rev = round(p.planned_revenue * b2c_share, 2)
    
    total_expenses_net = round(p.expenses_operating + p.investments, 2)
    
    tax_in = p.input_tax_rate if p.input_tax_rate is not None else cfg.VAT_STANDARD
    tax_out = p.output_tax_rate if p.output_tax_rate is not None else cfg.VAT_STANDARD
    
    # 1. Vorsteuer-Abzugspotenzial bei Regelbesteuerung
    # Vorsteuer = Ausgaben (Netto) * Vorsteuersatz
    input_tax_deductible = round(total_expenses_net * tax_in, 2)
    
    # 2. B2C-Margenvorteil der Kleinunternehmerregelung
    # Bei Endverbrauchern (B2C) zählt der Endpreis (Brutto).
    # Als Kleinunternehmer muss keine USt abgeführt werden.
    # Steueranteil im B2C-Bruttoumsatz = b2c_rev * (tax_out / (1 + tax_out))
    # Dies ist der Betrag, den der Kleinunternehmer behält, während der Regelbesteuerte ihn abführen muss.
    output_tax_b2c = round(b2c_rev * (tax_out / (1.0 + tax_out)), 2)
    
    # 3. Verwaltungskosten / Bürokratieaufwand
    # Als Kleinunternehmer entfallen unterjährige Voranmeldungen und komplexe USt-Erklärungen.
    admin_saved = round(p.admin_cost_standard_tax, 2)
    
    # 4. Gesamtwirtschaftlicher Netto-Vorteil der Kleinunternehmerregelung
    # Positiv = Kleinunternehmerregelung bringt mehr Nettoertrag
    # Negativ = Regelbesteuerung (Verzicht auf Befreiung) bringt mehr Nettoertrag
    net_advantage = round((output_tax_b2c + admin_saved) - input_tax_deductible, 2)
    
    # 5. Break-Even-Analysen
    # Break-Even-Investition: Ab welcher Investitionshöhe wird Vorsteuerabzug lukrativer?
    # Bedingung: (expenses_operating + break_even_investments) * tax_in = output_tax_b2c + admin_saved
    if tax_in > 0:
        needed_total_expenses = (output_tax_b2c + admin_saved) / tax_in
        break_even_investments = max(0.0, round(needed_total_expenses - p.expenses_operating, 2))
    else:
        break_even_investments = 0.0
        
    # Break-Even-B2B-Anteil: Ab welchem B2B-Anteil kippt die Entscheidung?
    # output_tax_b2c = planned_revenue * (1 - b2b_share) * (tax_out / (1 + tax_out))
    # Setze Gleichung: planned_revenue * (1 - b2b_share) * factor + admin_saved = input_tax_deductible
    tax_factor = (tax_out / (1.0 + tax_out)) if (1.0 + tax_out) > 0 else 0.0
    if p.planned_revenue > 0 and tax_factor > 0:
        # (1 - b2b_share) = (input_tax_deductible - admin_saved) / (planned_revenue * tax_factor)
        target_b2c_part = (input_tax_deductible - admin_saved) / (p.planned_revenue * tax_factor)
        calc_b2b_pct = (1.0 - target_b2c_part) * 100.0
        break_even_b2b_share_pct = max(0.0, min(100.0, round(calc_b2b_pct, 1)))
    else:
        break_even_b2b_share_pct = 50.0

    # 6. Empfehlungsfindung & Begründung
    reasons: List[str] = []
    
    if net_advantage > 150.0:
        rec = "KLEINUNTERNEHMER"
        badge_color = "green"
        rec_title = "Kleinunternehmerregelung klar empfohlen"
        rec_text = (
            f"Sie erzielen mit der Kleinunternehmerregelung einen geschätzten Netto-Vorteil von "
            f"+{net_advantage:,.2f} {cfg.CURRENCY} pro Jahr. Da Sie {(b2c_share * 100.0):.0f} % Ihrer Umsätze "
            f"an Privatkunden (B2C) erbringen, überwiegt die gesparte USt-Abführung den entgangenen Vorsteuerabzug."
        )
        reasons.append(f"Hoher B2C-Margenvorteil: +{output_tax_b2c:,.2f} {cfg.CURRENCY} USt verbleibt im Unternehmen.")
        reasons.append(f"Geringere Bürokratiekosten: ca. +{admin_saved:,.2f} {cfg.CURRENCY} Ersparnis bei USt-Voranmeldungen.")
        reasons.append(f"Entgangener Vorsteuerabzug (-{input_tax_deductible:,.2f} {cfg.CURRENCY}) wird durch B2C-Vorteil voll kompensiert.")
    elif net_advantage < -150.0:
        rec = "REGELBESTEUERUNG"
        badge_color = "blue"
        rec_title = "Regelbesteuerung / Vorsteuerabzug empfohlen"
        rec_text = (
            f"Die Regelbesteuerung verschafft Ihnen einen finanziellen Vorteil von "
            f"+{abs(net_advantage):,.2f} {cfg.CURRENCY} pro Jahr! Durch hohe Betriebsausgaben bzw. Investitionen "
            f"({total_expenses_net:,.2f} {cfg.CURRENCY}) und einen hohen B2B-Kundenanteil ({p.b2b_share_pct:.0f} %) "
            f"lohnt sich der freiwillige Verzicht auf die Kleinunternehmerregelung (§ 19 Abs. 2 UStG)."
        )
        reasons.append(f"Erheblicher Vorsteuer-Rückerstattungsanspruch: +{input_tax_deductible:,.2f} {cfg.CURRENCY} vom Finanzamt.")
        reasons.append(f"B2B-Kunden ({b2b_rev:,.2f} {cfg.CURRENCY}) können USt als Vorsteuer abziehen – kein Wettbewerbsnachteil.")
        reasons.append(f"Investitionen in Höhe von {p.investments:,.2f} {cfg.CURRENCY} sind netto 19 % / 20 % günstiger.")
    else:
        rec = "NEUTRAL"
        badge_color = "amber"
        rec_title = "Wirtschaftlich ausgeglichen (Grenzbereich)"
        rec_text = (
            f"Der rechnerische Unterschied liegt bei lediglich {net_advantage:,.2f} {cfg.CURRENCY} pro Jahr. "
            f"Treffen Sie die Entscheidung nach strategischen Kriterien (z.B. bürokratischer Aufwand vs. professionelles B2B-Image)."
        )
        reasons.append("Vorsteuererstattung und B2C-USt-Ersparnis halten sich nahezu die Waage.")
        reasons.append("Kleinunternehmerregelung spart Arbeitszeit; Regelbesteuerung bindet Sie 5 Jahre lang.")

    detailed_table = {
        "ku_brutto_umsatz": p.planned_revenue,
        "ku_ust_zahllast": 0.0,
        "ku_vorsteuer_abzug": 0.0,
        "ku_ausgaben_brutto": round(total_expenses_net * (1.0 + tax_in), 2),
        "ku_admin_kosten": 0.0,
        "ku_reingewinn_liquiditaet": round(p.planned_revenue - (total_expenses_net * (1.0 + tax_in)), 2),
        
        "regel_brutto_umsatz": round(b2c_rev + (b2b_rev * (1.0 + tax_out)), 2),
        "regel_ust_zahllast": output_tax_b2c,
        "regel_vorsteuer_abzug": input_tax_deductible,
        "regel_ausgaben_netto": total_expenses_net,
        "regel_admin_kosten": admin_saved,
        "regel_reingewinn_liquiditaet": round(
            (p.planned_revenue - output_tax_b2c) - total_expenses_net - admin_saved, 2
        ),
    }

    return ProfitabilityComparisonResult(
        country=p.country,
        currency=cfg.CURRENCY,
        currency_symbol=cfg.CURRENCY_SYMBOL,
        planned_revenue=p.planned_revenue,
        b2b_share_pct=p.b2b_share_pct,
        b2c_share_pct=round(100.0 - p.b2b_share_pct, 1),
        b2b_revenue=b2b_rev,
        b2c_revenue=b2c_rev,
        expenses_operating_net=p.expenses_operating,
        investments_net=p.investments,
        total_expenses_net=total_expenses_net,
        input_tax_rate=tax_in,
        output_tax_rate=tax_out,
        input_tax_deductible=input_tax_deductible,
        output_tax_b2c=output_tax_b2c,
        admin_cost_diff=admin_saved,
        net_advantage_kleinunternehmer=net_advantage,
        recommendation=rec,
        recommendation_title=rec_title,
        recommendation_text=rec_text,
        badge_color=badge_color,
        break_even_investments=break_even_investments,
        break_even_b2b_share_pct=break_even_b2b_share_pct,
        summary_reasons=reasons,
        detailed_table=detailed_table,
    )


def calculate_break_even(params: ProfitabilityInput) -> Dict[str, float]:
    """Berechnet die isolierten Break-Even-Schwellen."""
    res = calculate_profitability(params)
    return {
        "break_even_investments": res.break_even_investments,
        "break_even_b2b_share_pct": res.break_even_b2b_share_pct,
        "current_net_advantage": res.net_advantage_kleinunternehmer,
    }
