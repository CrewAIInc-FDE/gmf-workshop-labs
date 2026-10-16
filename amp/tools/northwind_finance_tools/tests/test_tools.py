"""Run with: pytest  (from this folder, in an environment that has crewai installed)."""
import importlib
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from northwind_finance_tools import (  # noqa: E402
    CreditTierLookupTool,
    LoanPaymentCalculatorTool,
    PayoffQuoteTool,
)
from northwind_finance_tools.tools import (  # noqa: E402
    CREDIT_TIERS,
    amortize,
    lookup_tier,
    monthly_payment,
    payoff_quote,
)


# --- loan payment -----------------------------------------------------------------
def test_monthly_payment_known_value():
    # 24,500 at 7.5% over 60 months: standard annuity formula
    assert monthly_payment(24500, 7.5, 60) == 490.93


def test_zero_apr_splits_evenly():
    assert monthly_payment(12000, 0, 48) == 250.00
    result = amortize(12000, 0, 48)
    assert result["total_interest"] == 0.0


def test_schedule_balances_to_zero_and_totals_add_up():
    result = amortize(24500, 7.5, 60)
    rows = result["rows"]
    assert len(rows) == 60
    assert rows[-1]["balance"] == 0.0
    assert result["total_paid"] == pytest.approx(24500 + result["total_interest"], abs=0.01)
    assert sum(r["principal"] for r in rows) == pytest.approx(24500, abs=0.01)
    assert rows[0]["interest"] == 153.13  # 24500 * 0.075 / 12 = 153.125, rounded half up


def test_single_month_loan():
    result = amortize(1000, 12, 1)
    assert result["monthly_payment"] == 1010.00
    assert result["total_interest"] == 10.00


def test_loan_tool_text_has_fixed_labels():
    text = LoanPaymentCalculatorTool().run(principal=24500, apr=7.5, term_months=60, schedule_rows=2)
    assert "Monthly payment: $490.93" in text
    assert "Total interest:" in text
    assert text.count("\n") >= 8
    assert "1 | $490.93 | $153.13" in text


def test_loan_tool_without_schedule_has_no_rows():
    text = LoanPaymentCalculatorTool().run(principal=10000, apr=5, term_months=36)
    assert "schedule rows" not in text


@pytest.mark.parametrize(
    "kwargs",
    [
        {"principal": 0, "apr": 5, "term_months": 36},
        {"principal": 1000, "apr": -1, "term_months": 36},
        {"principal": 1000, "apr": 5, "term_months": 0},
        {"principal": 1000, "apr": 5, "term_months": 36, "schedule_rows": 99},
    ],
)
def test_loan_tool_rejects_bad_arguments(kwargs):
    with pytest.raises((ValidationError, ValueError)):
        LoanPaymentCalculatorTool().run(**kwargs)


# --- payoff quote -----------------------------------------------------------------
def test_payoff_quote_numbers():
    quote = payoff_quote(18250.40, 7.5, 10)
    assert quote["per_diem"] == 3.75  # 18250.40 * 0.075 / 365
    assert quote["accrued_interest"] == 37.50
    assert quote["payoff_amount"] == 18287.90


def test_payoff_includes_fees_and_zero_days():
    assert payoff_quote(5000, 9.0, 0, unpaid_fees=25)["payoff_amount"] == 5025.00


def test_payoff_tool_text():
    text = PayoffQuoteTool().run(balance=18250.40, apr=7.5, days_to_payoff=10)
    assert "Per diem (interest per day): $3.75" in text
    assert "Payoff amount: $18,287.90" in text


def test_payoff_tool_rejects_negative_days():
    with pytest.raises((ValidationError, ValueError)):
        PayoffQuoteTool().run(balance=1000, apr=5, days_to_payoff=-3)


# --- credit tier ------------------------------------------------------------------
@pytest.mark.parametrize(
    "score,tier",
    [(850, "Super prime"), (781, "Super prime"), (780, "Prime"), (661, "Prime"),
     (660, "Near prime"), (601, "Near prime"), (600, "Subprime"), (501, "Subprime"),
     (500, "Deep subprime"), (300, "Deep subprime")],
)
def test_tier_boundaries(score, tier):
    assert lookup_tier(score)[0] == tier


def test_tiers_cover_300_to_850_without_gaps_or_overlap():
    covered = []
    for _tier, low, high, apr_low, apr_high in CREDIT_TIERS:
        assert apr_low < apr_high
        covered.extend(range(low, high + 1))
    assert sorted(covered) == list(range(300, 851))


def test_tier_tool_is_labelled_illustrative():
    text = CreditTierLookupTool().run(credit_score=712)
    assert "Tier: Prime" in text
    assert "ILLUSTRATIVE" in text
    assert "6.5% to 9.5%" in text


def test_tier_tool_rejects_out_of_range_scores():
    with pytest.raises((ValidationError, ValueError)):
        CreditTierLookupTool().run(credit_score=900)


# --- publish contract -------------------------------------------------------------
def test_package_exports_valid_tools_for_publish():
    """`crewai tool publish` reads __all__ and keeps BaseTool subclasses."""
    package = importlib.import_module("northwind_finance_tools")
    assert sorted(package.__all__) == [
        "CreditTierLookupTool", "LoanPaymentCalculatorTool", "PayoffQuoteTool",
    ]
    for name in package.__all__:
        tool = getattr(package, name)()
        assert tool.description and tool.name
        assert tool.args_schema.model_fields
        for field in tool.args_schema.model_fields.values():
            assert field.description, f"{name}: every argument needs a description"
