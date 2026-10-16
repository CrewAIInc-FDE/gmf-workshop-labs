#!/usr/bin/env bash
# Checks the container is ready for the labs. Run: bash ~/scripts/verify.sh
set -u
pass=0; fail=0
check() { if eval "$2" >/dev/null 2>&1; then echo "PASS  $1"; pass=$((pass+1)); else echo "FAIL  $1"; fail=$((fail+1)); fi; }
check "running as the 'crew' user"            '[ "$(id -un)" = crew ]'
check "CrewAI CLI 1.15.23 installed"          'crewai --version | grep -q 1.15.23'
check "lab dependencies pre-installed"        '/home/crew/.venv/bin/python -c "import crewai, crewai_tools"'
# Offline: each lab passes the same validation `crewai deploy create` runs.
for lab in policy_qa intake_triage renewal_prep bring_your_own; do
  check "lab $lab passes crewai deploy validate" "cd /home/crew/lab/$lab && crewai deploy validate"
done
# Same way the CrewAI CLI connects: no proxy settings, public certificate authorities only.
cli_reach() { /home/crew/.venv/bin/python -c 'import httpx,sys; httpx.Client(trust_env=False,timeout=10).get(sys.argv[1])' "$1"; }
check "app.crewai.com reachable the way the CLI connects"   'cli_reach https://app.crewai.com'
check "login.crewai.com reachable the way the CLI connects" 'cli_reach https://login.crewai.com'
echo "----"; echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
