#!/usr/bin/env python
"""Run the crew.

Usage: crewai run, or uv run run_crew NW-60977
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

# .env lives in the repo root; walk up until we find it.
for parent in Path(__file__).resolve().parents:
    if (parent / ".env").exists():
        load_dotenv(parent / ".env")
        break

from renewal_prep.crew import RenewalPrepCrew  # noqa: E402

DEFAULTS = {"account_id": 'NW-60412'}
KEYS = ['account_id']


def run():
    inputs = dict(DEFAULTS)
    for key, value in zip(KEYS, sys.argv[1:]):
        inputs[key] = value
    result = RenewalPrepCrew().crew().kickoff(inputs=inputs)
    print("\n" + "=" * 70 + "\n")
    print(result.raw)


if __name__ == "__main__":
    run()
