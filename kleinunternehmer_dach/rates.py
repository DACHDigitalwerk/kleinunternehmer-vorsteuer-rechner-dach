# -*- coding: utf-8 -*-
"""
Amtliche Schwellenwerte, Toleranzgrenzen und USt-Sätze 2026 für DE, AT und CH.
Basis: EU-Kleinunternehmer-Richtlinie RL (EU) 2020/285, § 19 UStG n.F. (DE),
§ 6 Abs. 1 Z 27 UStG n.F. (AT) sowie Art. 10 & 37 MWSTG (CH).
"""

from typing import Dict, Any


class GermanyRates:
    COUNTRY = "DE"
    NAME = "Deutschland"
    CURRENCY = "EUR"
    CURRENCY_SYMBOL = "€"
    
    # Grenzwerte 2026
    THRESHOLD_PREV_YEAR = 25000.0          # Angehoben von 22.000 €
    THRESHOLD_CURRENT_YEAR_NATIONAL = 25000.0
    THRESHOLD_EU_CROSSBORDER = 100000.0    # EU-Richtlinie 2026
    
    # Steuersätze
    VAT_STANDARD = 0.19                   # 19 % Regelsteuersatz
    VAT_REDUCED = 0.07                    # 7 % Ermäßigter Steuersatz
    
    LEGAL_BASIS = "§ 19 UStG n.F. (Wachstumschancengesetz & EU-RL 2020/285)"
    TYPICAL_ADMIN_COST_ANNUAL = 400.0     # Typische Mehrkosten USt-Voranmeldungen / StB


class AustriaRates:
    COUNTRY = "AT"
    NAME = "Österreich"
    CURRENCY = "EUR"
    CURRENCY_SYMBOL = "€"
    
    # Grenzwerte 2026
    THRESHOLD_STANDARD = 42000.0          # Angehoben von 35.000 €
    THRESHOLD_TOLERANCE = 55000.0         # Toleranzgrenze (1x in 5 Jahren)
    THRESHOLD_EU_CROSSBORDER = 100000.0   # EU-Richtlinie 2026
    
    # Steuersätze
    VAT_STANDARD = 0.20                   # 20 % Normalsteuersatz
    VAT_REDUCED_1 = 0.10                  # 10 % Ermäßigter Steuersatz
    VAT_REDUCED_2 = 0.13                  # 13 % Sondersatz
    
    LEGAL_BASIS = "§ 6 Abs. 1 Z 27 UStG n.F. (EU-AbgÄG 2024 / 2026)"
    TYPICAL_ADMIN_COST_ANNUAL = 450.0


class SwitzerlandRates:
    COUNTRY = "CH"
    NAME = "Schweiz"
    CURRENCY = "CHF"
    CURRENCY_SYMBOL = "CHF"
    
    # Grenzwerte 2026 (Art. 10 MWSTG)
    THRESHOLD_STANDARD = 100000.0         # 100.000 CHF weltweiter steuerbarer Umsatz
    THRESHOLD_NONPROFIT = 150000.0        # 150.000 CHF für gemeinnützige Sport-/Kulturvereine
    
    # Steuersätze 2026 (seit 01.01.2024 unverändert gültig für 2026)
    VAT_STANDARD = 0.081                  # 8,1 % Normalsatz
    VAT_SPECIAL_LODGING = 0.038           # 3,8 % Sondersatz Beherbergung
    VAT_REDUCED = 0.026                   # 2,6 % Reduzierter Satz (Güter d. Grundbedarfs)
    
    # Saldosteuersatzmethode (Art. 37 MWSTG) - typischer Dienstleister-Saldosatz
    SALDO_RATE_SERVICES = 0.060           # 6,0 % z.B. für Beratung, IT, Dienstleistungen
    SALDO_MAX_TURNOVER = 5005000.0        # Max. 5.005.000 CHF Umsatz
    SALDO_MAX_TAX_DUE = 103000.0          # Max. 103.000 CHF Steuerlast
    
    LEGAL_BASIS = "Art. 10, Art. 11 & Art. 37 MWSTG"
    TYPICAL_ADMIN_COST_ANNUAL = 500.0


COUNTRY_RATES_2026: Dict[str, Any] = {
    "DE": GermanyRates,
    "AT": AustriaRates,
    "CH": SwitzerlandRates,
}
