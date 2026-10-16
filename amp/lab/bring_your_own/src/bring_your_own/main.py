#!/usr/bin/env python
"""Entry point AMP uses to start the crew. In this lab, crews run on AMP, not on your laptop."""
from bring_your_own.crew import BringYourOwnCrew


def run():
    inputs = {"request": "What does Northwind's policy say about early payoff? Is there a prepayment penalty?"}
    return BringYourOwnCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
