---
description: API and schema contracts for merging upstream v3.0.22.
---

# merge-upstream-v3-0-22 Contracts

## API Contracts

No new API contract is approved merely by creating this scope. During the
merge, any upstream changes to route contracts must be reviewed against current
tests and docs before acceptance.

High-attention surfaces:

- Browser/auth routes under `backend_api_python/app/routes/`.
- Agent Gateway routes under `backend_api_python/app/routes/agent_v1/`.
- Broker/live-trading order submission routes and services.
- Billing, USDT payment, and notification endpoints.
- MCP tools under `mcp_server/src/quantdinger_mcp/`.

## Shared Types / Schemas

Schema and data compatibility checks must include:

- `backend_api_python/migrations/init.sql`.
- Any models or persistence helpers touched by upstream.
- Version constants managed by `scripts/check_version.py` and
  `scripts/bump_version.py`.
- Environment variables in `backend_api_python/env.example`.

## Event And Streaming Contracts

No event or streaming contract change is in scope unless upstream `v3.0.22`
touches those paths. If touched, add targeted tests or manual evidence before
closeout.

## Error Model

Security-sensitive errors must remain fail-closed:

- Invalid user JWTs and invalid agent tokens remain denied.
- Hosted/SaaS mode must not grant real-money trading scope by default.
- Credential decryption failures must not expose plaintext values.
- Strategy/indicator safe-exec failures must not escape sandbox restrictions.

## Validation And Compatibility Rules

- Use current source and runtime checks as the compatibility source of truth.
- Accept upstream behavior only after checking local security and product
  constraints.
- For documentation conflicts, preserve local wiki structure and move useful
  upstream durable knowledge into `.codex/wiki/`.
- For version conflicts, use repo scripts rather than manual-only edits.

## Requirement Boundary Notes

- This scope authorizes planning and later merge implementation; it does not
  authorize destructive history rewrites, production deployment, or secret
  rotation.
- If upstream tag verification fails, stop Phase 1 and record the exact remote
  evidence before asking for direction.
