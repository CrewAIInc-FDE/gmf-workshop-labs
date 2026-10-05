#!/usr/bin/env python
"""Run the crew.

Usage: crewai run, or uv run run_crew 12  (batch size)
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

# .env lives in the repo root; walk up until we find it.
for parent in Path(__file__).resolve().parents:
    if (parent / ".env").exists():
        load_dotenv(parent / ".env")
        break

from intake_triage.crew import IntakeTriageCrew  # noqa: E402

DEFAULTS = {"batch_size": '8'}
KEYS = ['batch_size']


def run():
    inputs = dict(DEFAULTS)
    for key, value in zip(KEYS, sys.argv[1:]):
        inputs[key] = value
    result = IntakeTriageCrew().crew().kickoff(inputs=inputs)
    print("\n" + "=" * 70 + "\n")
    print(result.raw)


if __name__ == "__main__":
    run()
