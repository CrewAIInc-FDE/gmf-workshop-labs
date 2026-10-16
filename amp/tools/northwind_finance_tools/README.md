# northwind_finance_tools

Three deterministic, keyless CrewAI tools for the Northwind Auto Finance workshop labs
(Northwind is a fictional lender; all data is synthetic).

| Tool class | Tool name the agent sees | What it does |
| --- | --- | --- |
| `LoanPaymentCalculatorTool` | `loan_payment_calculator` | principal, APR, term in months -> monthly payment, total interest, optional first N schedule rows |
| `PayoffQuoteTool` | `payoff_quote_calculator` | balance, APR, days to payoff, optional unpaid fees -> per diem and payoff amount (365-day year) |
| `CreditTierLookupTool` | `credit_tier_lookup` | credit score -> tier and an ILLUSTRATIVE APR band from a small fixed synthetic table |

No network, no API keys, no files. The same input always gives the same answer.

## Use them without publishing (works anywhere, including AMP)

Copy the package folder into your crew project and import it from there:

```bash
cp -r src/northwind_finance_tools  <your project>/src/<your_package>/
```

```python
from <your_package>.northwind_finance_tools import LoanPaymentCalculatorTool

Agent(..., tools=[LoanPaymentCalculatorTool()])
```

The package uses relative imports, so it works from any folder. Your project is deployed
with the copy inside it; nothing is installed from a registry.

## Use them from the org Tool Repository (after `crewai tool publish`)

```bash
crewai tool install northwind-finance-tools   # AMP turns the underscores into hyphens
```

```python
from northwind_finance_tools import LoanPaymentCalculatorTool, PayoffQuoteTool, CreditTierLookupTool
```

## Test

```bash
python -m pytest        # in an environment with crewai installed
```

## Layout (what `crewai tool publish` expects)

- `pyproject.toml` with `name`, `version`, and `[tool.crewai] type = "tool"`
- `src/<package>/__init__.py` that lists every tool class in `__all__`
  (every `__init__.py` under `src/` must define `__all__`)
- tool classes that inherit `crewai.tools.BaseTool` (or `@tool` functions)
- a git repository with all changes committed (a local commit is enough; publish refuses a dirty tree)
- do not pin `crewai` to one exact version in `dependencies` (Studio runs a different CrewAI
  version and fails with `Failed to run automation (500)`); `crewai>=1.10` works
