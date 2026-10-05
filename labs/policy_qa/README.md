 # Lab 2 starter - Policy questions and answers

 One agent, one task, connected to Northwind's policy library through the workshop
 connector. It runs as-is. Your job is to make it trustworthy.

 Ideas, in rough order:
 1. Make the answer cite the policy id it relies on (edit `config/tasks.yaml`).
 2. Tell the agent to say "the policies don't cover this" instead of guessing.
 3. Try `search_policies` with `mode` keyword vs semantic vs hybrid, and different `top_k`.
 4. Add a second agent that reviews the answer against the cited policy before it goes out.

 The finished version is in `reference/policy_qa`.

## Run it

```bash
cd labs/policy_qa
crewai install      # first time only, about a minute
crewai run          # uses the default inputs in src/policy_qa/main.py
```

Or pass your own input: `uv run run_crew "Is there a fee to pay my loan off early?"`
