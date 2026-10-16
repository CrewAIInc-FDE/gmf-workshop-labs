"""Three deterministic auto-finance tools for Northwind Auto Finance (a fictional lender).

Design rules, so an agent can use them reliably:
- Keyless and offline: no network, no API keys, no files.
- Deterministic: the same arguments always give the same answer.
- Plain-text results with fixed labels, so the agent can quote them exactly.
- Money is rounded to cents; APR is a percent (7.5 means 7.5 percent a year).

The math lives in small plain functions (`amortize`, `payoff_quote`, `lookup_tier`) so it
can be tested without an agent. The tool classes only validate arguments and format text.
"""
from __future__ import annotations

from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------------------
# Illustrative credit tiers. SYNTHETIC: not a real rate sheet and not an offer of credit.
# (tier, min score, max score, APR low %, APR high %) for a 60-month used-vehicle loan.
# The workshop's byo-files/rate_sheet.xlsx is generated from this same table.
# ---------------------------------------------------------------------------------------
CREDIT_TIERS: list[tuple[str, int, int, float, float]] = [
    ("Super prime", 781, 850, 4.5, 6.5),
    ("Prime", 661, 780, 6.5, 9.5),
    ("Near prime", 601, 660, 9.5, 14.0),
    ("Subprime", 501, 600, 14.0, 19.5),
    ("Deep subprime", 300, 500, 19.5, 24.0),
]
TIER_DISCLAIMER = (
    "ILLUSTRATIVE ONLY: a small synthetic Northwind table for the workshop, "
    "not a real rate sheet and not an offer of credit."
)
DAYS_IN_YEAR = 365  # per-diem interest uses a 365-day year


def _cents(value: float) -> float:
    return round(value + 1e-9, 2)


def money(value: float) -> str:
    return f"${value:,.2f}"


# ------------------------------------------------------------------ pure functions ----
def monthly_payment(principal: float, apr: float, term_months: int) -> float:
    """Level monthly payment for a fully amortizing loan, rounded to cents."""
    rate = apr / 100 / 12
    if rate == 0:
        return _cents(principal / term_months)
    factor = (1 + rate) ** term_months
    return _cents(principal * rate * factor / (factor - 1))


def amortize(principal: float, apr: float, term_months: int) -> dict[str, Any]:
    """Build the full schedule. The final payment is adjusted so the balance ends at 0.00."""
    rate = apr / 100 / 12
    payment = monthly_payment(principal, apr, term_months)
    balance = principal
    rows: list[dict[str, float | int]] = []
    total_interest = 0.0
    total_paid = 0.0
    for month in range(1, term_months + 1):
        interest = _cents(balance * rate)
        paid = payment if month < term_months else _cents(balance + interest)
        principal_part = _cents(paid - interest)
        balance = _cents(balance - principal_part)
        total_interest += interest
        total_paid += paid
        rows.append(
            {
                "month": month,
                "payment": paid,
                "interest": interest,
                "principal": principal_part,
                "balance": max(balance, 0.0),
            }
        )
    return {
        "monthly_payment": payment,
        "final_payment": rows[-1]["payment"],
        "total_interest": _cents(total_interest),
        "total_paid": _cents(total_paid),
        "rows": rows,
    }


def payoff_quote(
    balance: float, apr: float, days_to_payoff: int, unpaid_fees: float = 0.0
) -> dict[str, float]:
    """Payoff = balance + simple interest accrued over the days + unpaid fees."""
    per_diem = balance * apr / 100 / DAYS_IN_YEAR
    accrued = _cents(per_diem * days_to_payoff)
    return {
        "per_diem": _cents(per_diem),
        "accrued_interest": accrued,
        "unpaid_fees": _cents(unpaid_fees),
        "payoff_amount": _cents(balance + accrued + unpaid_fees),
    }


def lookup_tier(score: int) -> tuple[str, int, int, float, float]:
    for row in CREDIT_TIERS:
        if row[1] <= score <= row[2]:
            return row
    raise ValueError(f"score {score} is outside 300-850")


# --------------------------------------------------------------------------- tools -----
class LoanPaymentInput(BaseModel):
    """Arguments for the loan payment calculator."""

    principal: float = Field(
        ..., gt=0, le=10_000_000, description="Amount financed in dollars, for example 24500."
    )
    apr: float = Field(
        ...,
        ge=0,
        le=60,
        description="Annual percentage rate as a percent, for example 7.5 for 7.5 percent. Use 0 for a 0 percent loan.",
    )
    term_months: int = Field(
        ..., ge=1, le=120, description="Loan term in months, for example 60."
    )
    schedule_rows: int = Field(
        default=0,
        ge=0,
        le=24,
        description="How many of the first schedule rows to include (0 to 24). Use 0 if you only need the payment and totals.",
    )


class LoanPaymentCalculatorTool(BaseTool):
    name: str = "loan_payment_calculator"
    description: str = (
        "Calculates the level monthly payment, total interest and total paid for a fixed-rate "
        "auto loan, and can list the first few amortization rows (payment, interest, principal, "
        "remaining balance). Use it whenever you need a loan payment or interest cost: do not "
        "do this arithmetic yourself. Give principal in dollars, apr as a percent (7.5 means "
        "7.5 percent), and term in months."
    )
    args_schema: type[BaseModel] = LoanPaymentInput

    def _run(
        self, principal: float, apr: float, term_months: int, schedule_rows: int = 0
    ) -> str:
        result = amortize(principal, apr, term_months)
        lines = [
            f"Principal: {money(principal)}",
            f"APR: {apr:g}%",
            f"Term: {term_months} months",
            f"Monthly payment: {money(result['monthly_payment'])}",
            f"Final payment: {money(result['final_payment'])}",
            f"Total of payments: {money(result['total_paid'])}",
            f"Total interest: {money(result['total_interest'])}",
        ]
        if schedule_rows:
            lines.append(f"First {min(schedule_rows, term_months)} schedule rows (month | payment | interest | principal | balance):")
            for row in result["rows"][:schedule_rows]:
                lines.append(
                    f"{row['month']} | {money(row['payment'])} | {money(row['interest'])} | "
                    f"{money(row['principal'])} | {money(row['balance'])}"
                )
        return "\n".join(lines)


class PayoffQuoteInput(BaseModel):
    """Arguments for the payoff quote calculator."""

    balance: float = Field(
        ..., ge=0, le=10_000_000, description="Current principal balance in dollars, for example 18250.40."
    )
    apr: float = Field(
        ..., ge=0, le=60, description="Annual percentage rate as a percent, for example 7.5."
    )
    days_to_payoff: int = Field(
        ...,
        ge=0,
        le=365,
        description="Number of days from the balance date until the payoff funds arrive, for example 10.",
    )
    unpaid_fees: float = Field(
        default=0.0, ge=0, description="Any unpaid fees in dollars to add to the payoff. Default 0."
    )


class PayoffQuoteTool(BaseTool):
    name: str = "payoff_quote_calculator"
    description: str = (
        "Calculates a loan payoff amount: balance plus simple interest accrued over the number "
        "of days to payoff (using a 365-day year) plus any unpaid fees. Also returns the per "
        "diem, the interest per day, so the payer can adjust for a delay. Use it for payoff "
        "quotes: do not do this arithmetic yourself. It does not check authorization or "
        "eligibility - apply the written payoff policy for that."
    )
    args_schema: type[BaseModel] = PayoffQuoteInput

    def _run(
        self, balance: float, apr: float, days_to_payoff: int, unpaid_fees: float = 0.0
    ) -> str:
        quote = payoff_quote(balance, apr, days_to_payoff, unpaid_fees)
        return "\n".join(
            [
                f"Principal balance: {money(balance)}",
                f"APR: {apr:g}%",
                f"Days to payoff: {days_to_payoff}",
                f"Per diem (interest per day): {money(quote['per_diem'])}",
                f"Accrued interest: {money(quote['accrued_interest'])}",
                f"Unpaid fees: {money(quote['unpaid_fees'])}",
                f"Payoff amount: {money(quote['payoff_amount'])}",
                "Method: accrued interest = balance x APR x days / 365, rounded once to cents.",
            ]
        )


class CreditTierInput(BaseModel):
    """Arguments for the credit tier lookup."""

    credit_score: int = Field(
        ..., ge=300, le=850, description="A credit score from 300 to 850, for example 712."
    )


class CreditTierLookupTool(BaseTool):
    name: str = "credit_tier_lookup"
    description: str = (
        "Looks up a credit score in a small ILLUSTRATIVE Northwind table and returns the credit "
        "tier and an example APR band for a 60-month loan. The table is synthetic for the "
        "workshop: it is not a real rate sheet and not an offer of credit, so always say the "
        "band is illustrative. Give a credit score from 300 to 850."
    )
    args_schema: type[BaseModel] = CreditTierInput

    def _run(self, credit_score: int) -> str:
        tier, low_score, high_score, apr_low, apr_high = lookup_tier(credit_score)
        return "\n".join(
            [
                f"Credit score: {credit_score}",
                f"Tier: {tier} (scores {low_score}-{high_score})",
                f"Illustrative APR band (60 months): {apr_low:.1f}% to {apr_high:.1f}%",
                TIER_DISCLAIMER,
            ]
        )
