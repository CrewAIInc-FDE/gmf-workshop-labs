# Renewal prep on AMP

A crew that prepares end-of-term outreach for Northwind Auto Finance customers whose
agreements are about to expire (fictional data). You edit it here and run it on CrewAI
AMP - never on this machine.

```bash
crewai deploy create                                   # first time: uploads this folder to AMP
crewai deploy push --uuid "$RENEWAL_PREP_DEPLOYMENT_ID"      # after each edit: uploads your changes
crewai deploy status --uuid "$RENEWAL_PREP_DEPLOYMENT_ID"    # is it Online yet?
```

Always pass `--uuid` with your own deployment id: everyone's project is named `renewal_prep`.
The lab guide walks through every step.
