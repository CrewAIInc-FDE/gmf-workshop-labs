#!/usr/bin/env bash
cat <<'EOF'

  -- CrewAI Workshop: GM Financial ------------------------------------------
  Everything is installed. Two steps before your first run:

   1. Open the file  .env  (it is already open in a tab) and paste the
      OpenAI key from the screen at the front of the room after
      OPENAI_API_KEY=   Paste into the FILE, not this terminal. Save.

   2. Check you can reach everything:     bash scripts/preflight.sh

  Then pick a lab:
      cd labs/policy_qa      &&  crewai run     (policy questions, citations)
      cd labs/intake_triage  &&  crewai run     (document intake triage)
      cd labs/renewal_prep   &&  crewai run     (renewal outreach)
      cd labs/bring_your_own &&  crewai run     (your own problem)

  Finished versions to compare against are in  reference/
  ----------------------------------------------------------------------------

EOF
