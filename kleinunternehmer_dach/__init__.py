# -*- coding: utf-8 -*-
"""
DACH Kleinunternehmer- & USt-Vorsteuer-Rechner 2026 (EU-Kleinunternehmer-Richtlinie DE, AT, CH)
Rechtssichere Schwellenwertprüfungen und Vorsteuer-Rentabilitätsanalysen.
"""

__version__ = "1.0.0"
__author__ = "DACH Digitalwerk"
__license__ = "MIT"

from .rates import (
    COUNTRY_RATES_2026,
    GermanyRates,
    AustriaRates,
    SwitzerlandRates,
)
from .models import (
    ProfitabilityInput,
    ProfitabilityComparisonResult,
    ThresholdCheckResult,
)
from .calculator import (
    check_threshold,
    calculate_profitability,
    calculate_break_even,
)
from .validator import (
    validate_profitability_input,
    validate_threshold_input,
)

__all__ = [
    "COUNTRY_RATES_2026",
    "GermanyRates",
    "AustriaRates",
    "SwitzerlandRates",
    "ProfitabilityInput",
    "ProfitabilityComparisonResult",
    "ThresholdCheckResult",
    "check_threshold",
    "calculate_profitability",
    "calculate_break_even",
    "validate_profitability_input",
    "validate_threshold_input",
]
