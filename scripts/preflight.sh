#!/usr/bin/env bash
# Workshop preflight: can this machine reach everything the workshop needs?
# Run it in a Codespace, or on a Mac/Linux laptop:  bash scripts/preflight.sh
# (On Windows use scripts/preflight.ps1.)  Prints PASS/FAIL per check and, at the end,
# the hostnames to hand to your network team if anything failed.
set -u
cd "$(dirname "$0")/.." 2>/dev/null || true
[ -f .env ] && set -a && . ./.env 2>/dev/null && set +a
MCP_URL="${MCP_URL:-https://d3m5dyfy6s31ka.cloudfront.net/mcp}"
BASE="${MCP_URL%/mcp}"
FAILED=()

code() { curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$@" 2>/dev/null || echo 000; }

check_reach() { # name url  -> any HTTP answer counts as reachable
  local c; c=$(code -I "$2"); [ "$c" = "000" ] && c=$(code "$2")
  if [ "$c" != "000" ]; then printf 'PASS  %-34s (HTTP %s)\n' "$1" "$c"
  else printf 'FAIL  %-34s no connection\n' "$1"; FAILED+=("$(echo "$2" | sed -E 's#https?://([^/]+).*#\1#')"); fi
}

echo "Workshop preflight - $(date '+%Y-%m-%d %H:%M')"
echo
check_reach "CrewAI Studio (app.crewai.com)"   https://app.crewai.com/
check_reach "PyPI index (pypi.org)"            https://pypi.org/simple/crewai/
check_reach "PyPI files"                        https://files.pythonhosted.org/
check_reach "GitHub"                            https://github.com/
check_reach "GitHub Codespaces"                 https://github.com/codespaces
check_reach "OpenAI API"                        https://api.openai.com/v1/models

# Workshop data connector: health JSON, then a real MCP handshake.
h=$(curl -s --max-time 15 "$BASE/health" 2>/dev/null)
if echo "$h" | grep -q '"status":"ok"'; then echo "PASS  Workshop data connector (health)"
else echo "FAIL  Workshop data connector (health)"; FAILED+=("$(echo "$BASE" | sed -E 's#https?://##')"); fi
init='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"preflight","version":"1"}}}'
r=$(curl -s --max-time 15 -X POST "$MCP_URL" -H 'Content-Type: application/json' \
      -H 'Accept: application/json, text/event-stream' -d "$init" 2>/dev/null)
if echo "$r" | grep -q 'northwind-workshop'; then echo "PASS  Workshop data connector (MCP handshake)"
else echo "FAIL  Workshop data connector (MCP handshake)"; fi

# The OpenAI key, if one is set: a 200 means the key works from here.
if [ -n "${OPENAI_API_KEY:-}" ]; then
  c=$(code https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY")
  [ "$c" = "200" ] && echo "PASS  OpenAI key accepted" || echo "FAIL  OpenAI key (HTTP $c) - check the key in .env"
else
  echo "SKIP  OpenAI key not set yet (paste it into .env)"
fi

echo
if [ ${#FAILED[@]} -eq 0 ]; then echo "All network checks passed."
else
  echo "Blocked from this network. Ask your network team to allow HTTPS (443) to:"
  printf '  %s\n' $(printf '%s\n' "${FAILED[@]}" | sort -u)
  exit 1
fi
