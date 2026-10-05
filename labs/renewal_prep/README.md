 # Lab 3 starter - Renewal preparation

 One agent drafts outreach for one account. It runs as-is. Make it something a retention
 team would actually send.

 Ideas, in rough order:
 1. Ground the options in policy: search the policies for end-of-term and loyalty rules.
 2. Treat customers differently by payment history (`late_payments_12m`, payment statuses).
 3. Respect `preferred_contact` - an email reads differently from a call script.
 4. Work a list: `list_expiring_agreements` with `as_of` 2026-11-03 and `within_days` 120.
 5. Add a reviewer that removes any promise the policies don't support.

 The finished version is in `reference/renewal_prep`.

## Run it

```bash
cd labs/renewal_prep
crewai install      # first time only, about a minute
crewai run          # uses the default inputs in src/renewal_prep/main.py
```

Or pass your own input: `uv run run_crew "NW-60977"`
