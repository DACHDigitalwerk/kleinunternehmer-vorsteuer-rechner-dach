# -*- coding: utf-8 -*-
"""
Eingabe-Validierungslogik für Schwellenwert- und Rentabilitätsberechnungen.
"""

from typing import Tuple
from .models import ProfitabilityInput
from .rates import COUNTRY_RATES_2026


def validate_country(country: str) -> str:
    """Validiert den Ländercode (DE, AT, CH)."""
    c = str(country).strip().upper()
    if c not in COUNTRY_RATES_2026:
        raise ValueError(
            f"Ungültiger Ländercode '{country}'. Unterstützt werden: {list(COUNTRY_RATES_2026.keys())}."
        )
    return c


def validate_threshold_input(
    country: str,
    prev_year_turnover: float,
    current_year_turnover: float
) -> Tuple[str, float, float]:
    """Prüft numerische Eingaben für Schwellenwertprüfung."""
    c = validate_country(country)
    
    try:
        prev = float(prev_year_turnover)
        curr = float(current_year_turnover)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Umsätze müssen numerische Werte sein: {e}")
        
    if prev < 0:
        raise ValueError(f"Vorjahresumsatz darf nicht negativ sein (angegeben: {prev}).")
    if curr < 0:
        raise ValueError(f"Umsatz des laufenden Jahres darf nicht negativ sein (angegeben: {curr}).")
        
    return c, round(prev, 2), round(curr, 2)


def validate_profitability_input(params: ProfitabilityInput) -> ProfitabilityInput:
    """Validiert alle Parameter des ProfitabilityInput-Objekts."""
    params.country = validate_country(params.country)
    
    if params.planned_revenue < 0:
        raise ValueError("Geplanter Jahresumsatz darf nicht negativ sein.")
        
    if not (0.0 <= params.b2b_share_pct <= 100.0):
        raise ValueError(
            f"B2B-Anteil muss zwischen 0 und 100 % liegen (angegeben: {params.b2b_share_pct}%)."
        )
        
    if params.expenses_operating < 0:
        raise ValueError("Laufende Betriebsausgaben dürfen nicht negativ sein.")
        
    if params.investments < 0:
        raise ValueError("Investitionen dürfen nicht negativ sein.")
        
    if params.admin_cost_standard_tax < 0:
        raise ValueError("Verwaltungsmehrkosten dürfen nicht negativ sein.")
        
    rate_cfg = COUNTRY_RATES_2026[params.country]
    
    if params.output_tax_rate is None:
        params.output_tax_rate = rate_cfg.VAT_STANDARD
    elif params.output_tax_rate < 0 or params.output_tax_rate > 1.0:
        raise ValueError(f"Ausgangssteuersatz muss zwischen 0.0 und 1.0 liegen ({params.output_tax_rate}).")
        
    if params.input_tax_rate is None:
        params.input_tax_rate = rate_cfg.VAT_STANDARD
    elif params.input_tax_rate < 0 or params.input_tax_rate > 1.0:
        raise ValueError(f"Eingangssteuersatz muss zwischen 0.0 und 1.0 liegen ({params.input_tax_rate}).")
        
    return params
