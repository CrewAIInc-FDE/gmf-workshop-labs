"""Northwind Auto Finance workshop tools.

Three deterministic, keyless CrewAI tools for auto-finance arithmetic. Everything they
return is computed from the arguments or from a small illustrative table, so the same
input always gives the same answer. The data is synthetic.

`crewai tool publish` reads `__all__` here to find the tools, so every tool class must be
listed in it."""
from .tools import (
    CreditTierLookupTool,
    LoanPaymentCalculatorTool,
    PayoffQuoteTool,
)

__all__ = [
    "CreditTierLookupTool",
    "LoanPaymentCalculatorTool",
    "PayoffQuoteTool",
]
