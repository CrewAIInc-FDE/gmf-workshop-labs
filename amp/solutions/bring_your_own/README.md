# Bring your own - finished example: payoff quote desk

The `bring_your_own` template filled in for one example problem: a payoff desk rep gets a dealer's
request and needs the payoff figures plus what to confirm before sending a quote.

- `payoff_analyst` looks up the account (Northwind connector) and calls the **payoff quote calculator** tool.
- `quote_writer` reads the early payoff policy (POL-103) and writes the note.
- The calculator comes from `src/bring_your_own/northwind_finance_tools/`, a copy of the workshop tools
  package, so nothing needs to be installed or published.

Try this request in the AMP Run form (account NW-53318 has a balance of 16,976.40 at 6.9% APR):

```text
A dealer, Lakeside Motors, asks for a payoff quote on account NW-53318 for funds arriving in 10 days. The dealer has not sent written authorization from the customer.
```

Expected: payoff amount `$17,008.49`, per diem `$3.21`, and a "Confirm before sending" list that includes
the written authorization requirement (POL-103).

Deploy: `crewai deploy create`, then `crewai deploy push --uuid "$BYO_DEPLOYMENT_ID"` after edits.
