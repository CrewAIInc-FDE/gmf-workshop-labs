# CrewAI workshop labs - GM Financial, 2026-11-03

Hands-on labs for the afternoon build session. Everything here uses **Northwind Auto
Finance**, a fictional auto lender, and synthetic data. Never put GM Financial data in
this environment.

## Three ways to build

| Path | What you need | Start here |
| --- | --- | --- |
| **CrewAI Studio** (visual, no code) | A browser and the workshop Studio invite | The lab guide, "Studio" sections |
| **GitHub Codespace** (code, nothing to install) | A free GitHub account | Click **Code > Codespaces > Create codespace on main** |
| **Your own laptop** (code) | Python 3.10 to 3.13 and access to PyPI | "Local install" below |

## In a Codespace

The codespace installs everything for you (about two minutes the first time). When the
terminal shows the welcome message:

1. Paste the OpenAI key from the front of the room into the `.env` file after
   `OPENAI_API_KEY=` and save.
2. Run `bash scripts/preflight.sh` - every line should say PASS.
3. Pick a lab: `cd labs/policy_qa && crewai run`

## Local install

```bash
pip install uv                      # or: curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install crewai==1.15.23
cp .env.example .env                # then paste the OpenAI key into .env
bash scripts/preflight.sh           # Windows: powershell -ExecutionPolicy Bypass -File scripts\preflight.ps1
cd labs/policy_qa
crewai install
crewai run
```

If `pip` or `crewai install` cannot reach PyPI from your network, use a Codespace instead.

## The labs

| Lab | Folder | Finished version |
| --- | --- | --- |
| 1. Document intake triage | `labs/intake_triage` | `reference/intake_triage` |
| 2. Policy questions and answers | `labs/policy_qa` | `reference/policy_qa` |
| 3. Renewal preparation | `labs/renewal_prep` | `reference/renewal_prep` |
| 4. Bring your own | `labs/bring_your_own` | - |

Each starter runs as-is with one agent. The README in each folder lists what to try next.
The `reference/` versions are finished multi-agent crews: look at them if you get stuck,
step out, or want to compare.

## The data connector

All labs reach Northwind's data through one MCP server (`MCP_URL` in `.env`). Tools:

| Tool | What it does |
| --- | --- |
| `search_policies(query, top_k, mode)` | Search the policy library. `mode` is `semantic`, `keyword` or `hybrid` |
| `get_policy(policy_id)` / `list_policies()` | Read one policy / list them all |
| `list_inbox_documents()` / `get_inbox_document(doc_id)` | The shared intake inbox |
| `list_routing_queues()` / `route_document(doc_id, queue, reason, urgency)` | Work queues for triage (sandbox: nothing is stored) |
| `list_expiring_agreements(within_days, as_of)` / `get_client_account(account_id)` | Accounts and payment history |

The same connector is available in CrewAI Studio as **Northwind Workshop Data**.
