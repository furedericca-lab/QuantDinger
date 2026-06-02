---
description: API, documentation, and deployment contracts for merging upstream v3.0.27.
---

# merge-upstream-v3-0-27 Contracts

## API Contracts

This scope may accept upstream backend improvements through `v3.0.27`, but it
does not authorize restoring removed product surfaces.

Preserve:

- Auth, OAuth, user profile, credential, broker, strategy, indicator,
  backtest, experiment, market data, portfolio, notification, health, and
  Agent Gateway APIs.
- MCP behavior under `mcp_server/`.
- OpenAPI artifacts under `.codex/wiki/reference/api/` and
  `.codex/wiki/reference/agent/`.

Do not restore:

- Community marketplace routes/services/schema.
- Billing, credits, VIP, membership, or purchase endpoints.
- USDT payment routes, services, watchers, startup hooks, schema, or settings.
- Active legacy `docs/api`, `docs/agent`, or `docs/API_CONVENTIONS.md` paths.

## Documentation And Deployment Contracts

- Preserve the local Gunicorn/nginx/PostgreSQL/Redis single-user baseline.
- Preserve Cloudflare Tunnel hostname `https://tsw.momoe.qzz.io` unless the
  user separately changes Cloudflare.
- Preserve `frontend/` as the git submodule for Vue source.
- Do not restore Docker Compose, Dockerfile, GHCR publishing, Railway, or
  container-first deployment docs as active local baseline.
- Move useful upstream durable knowledge into `.codex/wiki/`; do not recreate
  the old `docs/` tree as active documentation.

## Frontend Contract

- Frontend source remote:
  `https://github.com/furedericca-lab/QuantDinger-Vue`.
- Current submodule baseline before this scope:
  `92e1da4c68d353505a3c1c04ad5a9a9f383d0540` (`v3.0.22`).
- Target frontend release line: `v3.0.27`.
- If the fork lacks a `v3.0.27` tag, use the matching reachable commit from
  the fork history and record the exact hash.

## Validation Rules

- Resolve merge conflicts with current source and archived local baselines as
  source of truth.
- Run focused tests for changed high-risk modules when feasible.
- Regenerate OpenAPI into the wiki path if backend API contracts change.
- Run wiki rebuild and doctor after docs/wiki changes.
- Run residual scans for restored billing/community/payment/docs/Docker
  surfaces before closeout.

## Stop Conditions

- The upstream tag cannot be verified.
- Merge resolution would require losing local security, secret-handling,
  runtime-safety, or no-paid-product baseline.
- Frontend `v3.0.27` cannot be located in the fork or safely built.
- Validation reveals behavior regressions that cannot be fixed within this
  scope.
