 # Lab 4 - Bring your own

 Start by writing the problem down, the way you would describe it to a new colleague:

 1. **Who** has this problem today, and how often?
 2. **What goes in**: documents, records, a question?
 3. **What comes out**: a decision, a draft, a table? Who reads it?
 4. **What does good enough look like?** How would you know it worked?
 5. **Should this be an agent at all?** If it is a script with three conditions, keep it a script.

 Then reshape this project: rename the agent, split the work into two or three agents with
 one job each, and write tasks whose expected output matches step 3. You can use the
 Northwind data through the connector, or no tools at all. Never paste GM Financial data
 into the workshop environment.

## Run it

```bash
cd labs/bring_your_own
crewai install      # first time only, about a minute
crewai run          # uses the default inputs in src/bring_your_own/main.py
```

Or pass your own input: `uv run run_crew "Draft a checklist for a new intake clerk"`
