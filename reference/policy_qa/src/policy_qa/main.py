#!/usr/bin/env python
"""Run the crew.

Usage: crewai run, or uv run run_crew "<question>"
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

# .env lives in the repo root; walk up until we find it.
for parent in Path(__file__).resolve().parents:
    if (parent / ".env").exists():
        load_dotenv(parent / ".env")
        break

from policy_qa.crew import PolicyQACrew  # noqa: E402

DEFAULTS = {"question": 'A customer lost their job last month and has never missed a payment. Can they defer their next two payments, and what happens to interest?'}
KEYS = ['question']


def run():
    inputs = dict(DEFAULTS)
    for key, value in zip(KEYS, sys.argv[1:]):
        inputs[key] = value
    result = PolicyQACrew().crew().kickoff(inputs=inputs)
    print("\n" + "=" * 70 + "\n")
    print(result.raw)


if __name__ == "__main__":
    run()
