# Reference - Policy questions and answers

Three agents: researcher, writer, reviewer. Compare with `labs/policy_qa`.

## Run it

```bash
cd reference/policy_qa
crewai install      # first time only, about a minute
crewai run          # uses the default inputs in src/policy_qa/main.py
```

Or pass your own input: `uv run run_crew "Is there a fee to pay my loan off early?"`
