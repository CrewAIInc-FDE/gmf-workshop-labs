#!/usr/bin/env python
"""Entry point AMP uses to start the crew. In this lab, crews run on AMP, not on your laptop."""
from policy_qa.crew import PolicyQACrew


def run():
    inputs = {"question": "A customer lost their job last month and has never missed a payment. Can they defer their next two payments?"}
    return PolicyQACrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
