# Bring your own - on AMP

A starter crew for your own problem, built on Northwind Auto Finance's sample data
(fictional). You edit it here and run it on CrewAI AMP - never on this machine.

```bash
crewai deploy create                                   # first time: uploads this folder to AMP
crewai deploy push --uuid "$BYO_DEPLOYMENT_ID"      # after each edit: uploads your changes
crewai deploy status --uuid "$BYO_DEPLOYMENT_ID"    # is it Online yet?
```

Always pass `--uuid` with your own deployment id: everyone's project is named `bring_your_own`.
Edit the parts marked `EDIT HERE` in `src/bring_your_own/config/agents.yaml` and `tasks.yaml`.
The lab guide walks through every step. Use only the sample data in this lab - never paste real
customer or company data.
