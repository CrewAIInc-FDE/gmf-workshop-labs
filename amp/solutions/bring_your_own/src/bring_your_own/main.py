#!/usr/bin/env python
"""Entry point AMP uses to start the crew. In this lab, crews run on AMP, not on your laptop."""
from bring_your_own.crew import BringYourOwnCrew


def run():
    inputs = {
        "request": "A dealer, Lakeside Motors, asks for a payoff quote on account NW-53318 "
        "for funds arriving in 10 days. The dealer has not sent written authorization from the customer."
    }
    return BringYourOwnCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
