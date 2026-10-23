# -*- coding: utf-8 -*-
"""
Datenmodelle für Schwellenwert-Validierung und Vorsteuer-Rentabilitätsrechnung.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class ThresholdCheckResult:
    """Ergebnis der Schwellenwert- und Berechtigungsprüfung."""
    country: str
    country_name: str
    currency: str
    currency_symbol: str
    prev_year_turnover: float
    current_year_turnover: float
    is_eligible: bool
    threshold_limit: float
    threshold_status: str  # "SAFE", "WARNING_NEAR_LIMIT", "EXCEEDED", "TOLERANCE_ZONE"
    utilization_pct: float
    message: str
    statutory_basis: str
    action_recommendations: List[str] = field(default_factory=list)
    legal_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProfitabilityInput:
    """Eingabeparameter für den Kleinunternehmer-Rentabilitätsvergleich."""
    country: str = "DE"
    planned_revenue: float = 24000.0
    b2b_share_pct: float = 30.0           # Anteil B2B in Prozent (0.0 bis 100.0)
    expenses_operating: float = 3500.0    # Laufende Betriebsausgaben (Netto)
    investments: float = 2000.0           # Investitionen / Anschaffungen (Netto)
    input_tax_rate: Optional[float] = None # Z.B. 0.19 für 19 %
    output_tax_rate: Optional[float] = None
    admin_cost_standard_tax: float = 400.0 # Mehrkosten USt-Voranmeldungen / StB
    is_nonprofit: bool = False             # Schweiz Sonderregelung für Vereine


@dataclass
class ProfitabilityComparisonResult:
    """Gegenüberstellung Kleinunternehmerregelung vs. Regelbesteuerung."""
    country: str
    currency: str
    currency_symbol: str
    planned_revenue: float
    b2b_share_pct: float
    b2c_share_pct: float
    b2b_revenue: float
    b2c_revenue: float
    
    # Betriebsausgaben
    expenses_operating_net: float
    investments_net: float
    total_expenses_net: float
    
    # Steuersätze
    input_tax_rate: float
    output_tax_rate: float
    
    # Vorsteuer & Zahllast
    input_tax_deductible: float           # Vorsteuer, die bei Regelbesteuerung erstattet wird
    output_tax_b2c: float                 # USt auf B2C-Umsätze, die bei Kleinunternehmer gespart wird
    admin_cost_diff: float                # Gesparte Verwaltungskosten bei Kleinunternehmer
    
    # Gesamtwirtschaftlicher Netto-Vorteil der Kleinunternehmerregelung
    # Formel: Netto-Vorteil = USt-Ersparnis B2C + Admin-Ersparnis - Entgangene Vorsteuer auf Ausgaben
    net_advantage_kleinunternehmer: float
    
    # Empfehlung
    recommendation: str                   # "KLEINUNTERNEHMER" oder "REGELBESTEUERUNG" oder "NEUTRAL"
    recommendation_title: str
    recommendation_text: str
    badge_color: str                      # "green", "blue", "amber"
    
    # Break-Even-Punkte
    break_even_investments: float         # Investitionshöhe, ab der Regelbesteuerung günstiger wird
    break_even_b2b_share_pct: float       # B2B-Anteil, ab dem Regelbesteuerung günstiger wird
    
    summary_reasons: List[str] = field(default_factory=list)
    detailed_table: Dict[str, Any] = field(default_factory=dict)
    rdg_disclaimer: str = (
        "Mathematische Simulation ohne Gewähr. Keine Rechts- oder Steuerberatung gem. § 2 RDG / § 5 StBerG."
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
