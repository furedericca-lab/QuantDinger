---
description: Research notes for slimming QuantDinger to a local nginx deployment without external monetization features.
---

# Implementation Research Notes: Local Nginx Slimdown

## Problem Statement And Current Baseline

QuantDinger currently carries two deployment and product modes that are no
longer aligned with the operator target for this checkout:

- Local production should be backend/Gunicorn plus local PostgreSQL, Redis, and
  nginx reverse proxy, not Docker Compose, Railway, GHCR publishing, or
  container-first install flows.
- External paid functionality is not needed. Community marketplace, billing,
  credits, VIP, membership purchase, and USDT payment flows should be removed.

Current durable docs still describe Docker Compose as the default runtime:
`README.md`, `AGENT.md`, `.codex/wiki/implementation/deployment-and-operations.md`,
`.codex/wiki/reference/current-verification-commands.md`, and
`.codex/wiki/reference/configuration-and-integrations.md`.

Features explicitly preserved by user decision:

- `mcp_server/` and Agent Gateway REST/MCP integration.
- Broker and live trading integrations, including IBKR, MT5, and Alpaca.
- OAuth, Turnstile, email, SMS, and Telegram notification support.
- Strategy, indicator, backtest, experiment, market data, and agent APIs.

## Gap Analysis With Evidence

- Deployment assets are still tracked as active runtime paths:
  `docker-compose.yml`, `docker-compose.build.yml`, `docker-compose.ghcr.yml`,
  `backend_api_python/Dockerfile`, `backend_api_python/docker-entrypoint.sh`,
  `install.sh`, `.github/workflows/docker-publish.yml`,
  `backend_api_python/railway.json`, and `mcp_server/railway.json`.
- `AGENT.md` lists Docker Compose files as top-level ownership and contains
  Docker deletion guardrails that must be rewritten for a local nginx baseline.
- `.codex/wiki/implementation/deployment-and-operations.md` and
  `.codex/wiki/reference/current-verification-commands.md` name Docker Compose
  as the current operator path and need replacement with systemd/Gunicorn/nginx
  checks.
- Community marketplace is centered on
  `backend_api_python/app/routes/community.py` and
  `backend_api_python/app/services/community_service.py`. It also touches
  OpenAPI registration in `backend_api_python/app/openapi/register.py` and
  community/purchase/comment tables and columns in
  `backend_api_python/migrations/init.sql`.
- Billing and credits are centered on
  `backend_api_python/app/routes/billing.py` and
  `backend_api_python/app/services/billing_service.py`, with call sites in
  auth registration, OAuth registration, fast analysis, strategy AI generation,
  portfolio monitoring, indicator AI generation, settings, and user admin
  routes.
- USDT payment is centered on
  `backend_api_python/app/services/usdt_payment_service.py`,
  `backend_api_python/app/services/usdt_payment/`, billing route subpaths, the
  startup worker in `backend_api_python/app/__init__.py`, and related env and
  schema entries.
- The string `USDT` is not a deletion key by itself. Trading, exchange symbols,
  quick trade, broker examples, and crypto pairs may legitimately use USDT and
  must remain unless they are part of payment or membership purchase.

## Architecture / Implementation Options And Trade-Offs

Option A: Keep Docker and billing disabled by configuration.

- Pros: lowest immediate code churn.
- Cons: keeps dead operator paths, stale docs, schema fields, and paid product
  semantics; future merges can accidentally revive the SaaS/payment surface.

Option B: Remove only deployment packaging first and defer paid feature removal.

- Pros: reduces infra clutter quickly.
- Cons: user has explicitly rejected waiting for Phase 4; keeps credits/VIP
  behavior in core AI and user flows.

Option C: Four-phase removal with explicit preserved boundaries.

- Pros: each high-risk area has a reviewable phase, tests can isolate route,
  schema, startup, and docs drift, and Phase 4 can deeply remove Billing,
  credits, and VIP without affecting brokers, OAuth, notifications, or MCP.
- Cons: requires careful residual scans and OpenAPI/wiki synchronization after
  each phase.

Selected option: Option C.

## Decision Roundtable

| Decision | Requirement Clarity | Evidence Strength | Evidence Source | Conflict | User-Intent Confidence | Implementation Confidence | Risk/Reversibility | Outcome | Confidence Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Preserve MCP and Agent Gateway while removing deployment clutter | 5 | 5 | User instruction, `mcp_server/`, `.codex/wiki/implementation/agent-gateway-and-mcp.md` | None | 5 | 5 | 4 | Preserve | MCP is a useful local integration layer and is not tied to Docker or billing. |
| Preserve IBKR, MT5, Alpaca, OAuth, Turnstile, email, SMS, and Telegram | 5 | 5 | User instruction, `AGENT.md`, broker/wiki pages | None | 5 | 5 | 3 | Preserve | These are runtime integrations for local deployment and should not be part of monetization cleanup. |
| Remove Docker/Railway/GHCR deployment assets | 5 | 5 | User instruction, `README.md`, `AGENT.md`, wiki deployment pages | None | 5 | 5 | 3 | Remove in Phase 1 | Local nginx reverse proxy is the target deployment; Docker is excess for this checkout. |
| Remove Community marketplace | 5 | 4 | Prior source analysis of community route/service/schema and billing dependency | None | 5 | 4 | 3 | Remove in Phase 2 | Marketplace is an external product/business feature and depends on billing/purchase semantics. |
| Remove USDT payment and membership purchase before deep billing removal | 5 | 4 | Prior source analysis of billing route subpaths, payment services, startup worker, env, schema | None | 5 | 4 | 3 | Remove in Phase 3 | Payment USDT is unrelated to crypto trading symbols and should be deleted as monetization code. |
| Deep remove Billing, credits, and VIP in Phase 4 without waiting period | 5 | 4 | User instruction plus prior source analysis of routes, services, schema, and call sites | None | 5 | 4 | 3 | Remove in Phase 4 | User explicitly does not need external paid functionality; Phase 4 must remove fields and calls, not merely disable settings. |

## Selected Design And Rationale

The implementation should proceed in four phases:

1. Convert the documented operator baseline to host-local backend/Gunicorn plus
   nginx reverse proxy and remove container/cloud distribution assets.
2. Remove Community marketplace APIs, services, schema pieces, OpenAPI entries,
   tests, and docs while preserving private indicator/workspace functionality.
3. Remove USDT payment and membership purchase workers, services, route
   subpaths, env/settings, tests, and schema entries without touching trading
   symbols or broker flows.
4. Deep remove Billing, credits, and VIP from routes, services, schema, users,
   AI feature gates, admin endpoints, settings, OpenAPI, docs, and tests.

Each phase must update `.codex/wiki/` and API artifacts when behavior changes.

## Test And Validation Strategy

Baseline docs and repository hygiene:

- `git diff --check`
- `bash /root/.codex/skills/repo-task-driven/scripts/doc_placeholder_scan.sh .codex/scopes/archive/local-nginx-slimdown`
- `bash /root/.codex/skills/repo-task-driven/scripts/decision_roundtable_check.sh .codex/scopes/archive/local-nginx-slimdown`
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json`
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json`

Backend and API contract checks after implementation phases:

- `.venv/bin/python -m pytest backend_api_python/tests/test_openapi.py -q`
- `.venv/bin/python -m pytest backend_api_python/tests/test_health.py backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py -q`
- `.venv/bin/python -m pytest backend_api_python/tests/test_backtest_execution.py -q`
- `cd backend_api_python && ../.venv/bin/python scripts/export_openapi.py --output ../.codex/wiki/reference/api/openapi.generated.yaml && diff -u ../.codex/wiki/reference/api/openapi.yaml ../.codex/wiki/reference/api/openapi.generated.yaml; rm -f ../.codex/wiki/reference/api/openapi.generated.yaml`
- `npx --yes @stoplight/spectral-cli@6.15.1 lint .codex/wiki/reference/api/openapi.yaml --ruleset .spectral.yaml`

Residual text scans after monetization phases:

- `rg -n "Community|marketplace|Billing|credits|VIP|membership|usdt_payment|USDT payment|insufficient_credits|check_and_consume|refund" backend_api_python README.md AGENT.md .codex/wiki`

The residual scan may return legitimate trading `USDT` references; each hit
must be reviewed before deletion.

## Risks, Assumptions, Unresolved Questions

- Schema cleanup is high risk because `backend_api_python/migrations/init.sql`
  is the first-boot canonical schema. Existing production database migrations
  may need a separate migration script if this local deployment already has
  historical billing/community tables.
- Frontend source is not visible as a first-class local module in this scope
  unless it exists under the checkout during implementation. Any API removal
  must still search for client calls in tracked frontend or static assets.
- OpenAPI artifacts under `.codex/wiki/reference/api/` are authoritative and
  must be regenerated or hand-synchronized after route removals.
- User has already resolved the largest product question: Phase 4 should not
  wait for runtime observation and should remove paid functionality deeply.


## Closeout Evidence

Status: complete on 2026-06-01.

Implementation removed Docker/Railway/GHCR deployment assets, Community marketplace routes/services/schema, USDT payment workers/routes/settings/schema, and Billing/credits/VIP/membership code paths. README, AGENT, wiki pages, and OpenAPI artifacts now describe the local Gunicorn/nginx, PostgreSQL, Redis, no-paid-product baseline.

Validation evidence is recorded in `task-plans/4phases-checklist.md` and includes compileall, health/OpenAPI/Agent Gateway/backtest tests, OpenAPI export, residual scans, and wiki rebuild/doctor.
