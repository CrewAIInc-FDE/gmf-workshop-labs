#!/usr/bin/env bash
# Runs once when the codespace is created (and during prebuilds, if enabled).
set -euo pipefail
echo "==> Installing uv"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
echo "==> Installing the CrewAI CLI (pinned to the workshop version)"
uv tool install crewai==1.15.23
echo "==> Installing every lab's dependencies so 'crewai run' starts straight away"
for d in labs/* reference/*; do
  (cd "$d" && uv sync --quiet) || echo "warning: could not pre-install $d"
done
echo "==> Done: $(crewai --version)"
