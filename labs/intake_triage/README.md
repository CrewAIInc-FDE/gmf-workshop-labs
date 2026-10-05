 # Lab 1 starter - Document intake triage

 One agent triages one document. It runs as-is. Make it useful for a real intake team.

 Ideas, in rough order:
 1. Extract fields too: customer name, account id, request type, urgency.
 2. Actually route it with `route_document`, giving a reason.
 3. Handle a batch: list the inbox and triage the first ten documents.
 4. Add a second agent that double-checks anything urgent, suspicious or about a regulator.
 5. Output one table a supervisor could scan in ten seconds.

 Watch for the tricky ones: a document in Spanish, a phishing-looking email, a document
 that belongs to another company, a duplicate. The finished version is in `reference/intake_triage`.

## Run it

```bash
cd labs/intake_triage
crewai install      # first time only, about a minute
crewai run          # uses the default inputs in src/intake_triage/main.py
```

Or pass your own input: `uv run run_crew "DOC-0012"`
