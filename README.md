# CrewAI workshop labs - 2026-11-04

Hands-on labs for the afternoon build session. Everything here uses **Northwind Auto
Finance**, a fictional auto lender, and synthetic data. Never put real customer or company data in
this environment.

## Where to start

- **Lab guides** (Code and Studio tracks): https://crewaiinc-fde.github.io/crewai-field-labs/workshops/
- **Teaching slides**: https://crewaiinc-fde.github.io/gmf-workshop-labs/ (built from `site/`)

The Code track runs in a dev container image on your laptop and deploys to CrewAI AMP; the lab
guides walk through it. The folders below are an earlier local-run version of the labs, kept for
reference.

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
