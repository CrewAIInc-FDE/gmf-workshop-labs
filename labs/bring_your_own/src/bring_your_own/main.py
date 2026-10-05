#!/usr/bin/env python
"""Run the crew.

Usage: crewai run, or uv run run_crew "<your problem>"
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

# .env lives in the repo root; walk up until we find it.
for parent in Path(__file__).resolve().parents:
    if (parent / ".env").exists():
        load_dotenv(parent / ".env")
        break

from bring_your_own.crew import BringYourOwnCrew  # noqa: E402

DEFAULTS = {"problem": 'Summarize which inbox documents received this month mention a payment problem, and what each customer is asking for.'}
KEYS = ['problem']


def run():
    inputs = dict(DEFAULTS)
    for key, value in zip(KEYS, sys.argv[1:]):
        inputs[key] = value
    result = BringYourOwnCrew().crew().kickoff(inputs=inputs)
    print("\n" + "=" * 70 + "\n")
    print(result.raw)


if __name__ == "__main__":
    run()
