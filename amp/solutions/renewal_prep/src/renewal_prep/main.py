#!/usr/bin/env python
"""Entry point AMP uses to start the crew. In this lab, crews run on AMP, not on your laptop."""
from renewal_prep.crew import RenewalPrepCrew


def run():
    inputs = {"as_of": "2026-11-03", "within_days": "90", "account_id": "NW-60412"}
    return RenewalPrepCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
