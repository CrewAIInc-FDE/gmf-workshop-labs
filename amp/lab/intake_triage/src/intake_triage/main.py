#!/usr/bin/env python
"""Entry point AMP uses to start the crew. In this lab, crews run on AMP, not on your laptop."""
from intake_triage.crew import IntakeTriageCrew


def run():
    inputs = {"doc_id": "DOC-0004"}
    return IntakeTriageCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
