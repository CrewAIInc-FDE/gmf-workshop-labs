# Reference - Document intake triage

Three agents: analyst, router, supervisor. Compare with `labs/intake_triage`.

## Run it

```bash
cd reference/intake_triage
crewai install      # first time only, about a minute
crewai run          # uses the default inputs in src/intake_triage/main.py
```

Or pass your own input: `uv run run_crew "12"`
