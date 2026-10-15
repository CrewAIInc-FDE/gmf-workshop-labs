# Policy Q&A on AMP

A crew that answers customer service questions from Northwind Auto Finance's policy library
(fictional data). You edit it here and run it on CrewAI AMP - never on this machine.

```bash
crewai deploy create                                   # first time: uploads this folder to AMP
crewai deploy push --uuid "$CREWAI_DEPLOYMENT_ID"      # after each edit: uploads your changes
crewai deploy status --uuid "$CREWAI_DEPLOYMENT_ID"    # is it Online yet?
```

Always pass `--uuid` with your own deployment id: everyone's project is named `policy_qa`.
The lab guide walks through every step.
