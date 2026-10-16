# Intake triage on AMP

A crew that reads a document from Northwind Auto Finance's intake inbox (fictional data) and
recommends which work queue should handle it. You edit it here and run it on CrewAI AMP - never
on this machine.

```bash
crewai deploy create                                   # first time: uploads this folder to AMP
crewai deploy push --uuid "$INTAKE_TRIAGE_DEPLOYMENT_ID"      # after each edit: uploads your changes
crewai deploy status --uuid "$INTAKE_TRIAGE_DEPLOYMENT_ID"    # is it Online yet?
```

Always pass `--uuid` with your own deployment id: everyone's project is named `intake_triage`.
The lab guide walks through every step.
