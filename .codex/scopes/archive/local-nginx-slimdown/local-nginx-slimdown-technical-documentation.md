---
description: Technical design for the local nginx slimdown and monetization removal.
---

# Technical Documentation: Local Nginx Slimdown

## Canonical Architecture

Target runtime:

- `backend_api_python/` runs as the Flask backend under Gunicorn or an
  equivalent host-local process manager.
- PostgreSQL and Redis are local services or explicit local-network services.
- nginx is the reverse proxy and static/frontend serving boundary.
- `mcp_server/` remains an optional MCP wrapper over Agent Gateway REST APIs.
- `.codex/wiki/` remains the durable project knowledge base and houses API
  artifacts under `.codex/wiki/reference/api/` and
  `.codex/wiki/reference/agent/`.

Removed runtime surfaces:

- Docker Compose and Docker build/deployment assets.
- Railway/GHCR publishing assets.
- Community marketplace.
- USDT payment and membership purchase workers.
- Billing, credits, and VIP enforcement.

## Key Constraints And Non-Goals

- Preserve broker integrations, especially IBKR, MT5, and Alpaca.
- Preserve OAuth, Turnstile, email, SMS, and Telegram.
- Preserve Agent Gateway and MCP safety boundaries.
- Do not remove crypto trading or market-data `USDT` symbol support.
- Do not restore the legacy `docs/` tree; synchronize durable docs into
  `.codex/wiki/`.
- Do not introduce external paid services, payment processors, or new
  microservices.

## Major Decisions and Trade-offs

- Host-local nginx replaces Docker Compose as the operator baseline. This
  reduces local deployment complexity at the cost of removing container
  convenience paths.
- Paid feature removal is deep, not configuration-only. This prevents dormant
  credits/VIP gates from affecting AI and analysis workflows.
- USDT payment deletion is separate from trading `USDT` symbol preservation.
  Implementation must delete payment-specific modules and routes, not broad
  symbol strings.
- Community marketplace deletion must preserve private indicator and strategy
  workspace behavior.

## Interfaces Between Components

Backend HTTP APIs:

- Preserved: auth, OAuth, credentials, strategies, indicators, backtests,
  experiments, portfolio, notifications, broker routes, Agent Gateway, health,
  settings that are not billing/payment-specific.
- Removed: Community marketplace endpoints, billing endpoints, USDT payment
  endpoints, credits/VIP admin endpoints, and membership purchase endpoints.

Schema:

- Preserve core users/auth/security fields, credentials, strategies, backtests,
  indicators, broker/session data, notifications, Agent Gateway artifacts, and
  market-data tables.
- Remove community purchase/comment/review tables and marketplace columns.
- Remove billing/credits/VIP columns and tables, including credit logs,
  membership orders, and USDT payment orders.

OpenAPI:

- Generated OpenAPI must match `.codex/wiki/reference/api/openapi.yaml`.
- Agent OpenAPI must remain available at
  `.codex/wiki/reference/agent/agent-openapi.json`.

## Operational Behavior

Startup after the scope completes:

- Backend starts without Docker entrypoint assumptions.
- No USDT order worker starts from `backend_api_python/app/__init__.py`.
- No billing configuration is required in `backend_api_python/env.example`.
- nginx proxies to the backend and serves the frontend/static route according
  to the updated README/wiki.
- MCP can be run against Agent Gateway using the preserved agent token flow.

Shutdown:

- There are no payment watchers or membership workers to stop.
- Existing broker and portfolio workers keep their current documented controls.

## Observability And Error Handling

- Health checks must continue to cover backend startup and database/Redis
  availability.
- Agent Gateway tests must continue to protect paper/live trading boundaries.
- AI, fast analysis, strategy, portfolio monitor, and indicator generation
  errors should be about provider/runtime failure, validation failure, or user
  input, not insufficient credits or VIP state.
- Settings endpoints should omit removed billing/payment settings instead of
  returning disabled placeholders.

## Security Model And Hardening Notes

- Removing billing/payment reduces secret surface by removing USDT watcher keys
  and receiving-address configuration.
- OAuth, Turnstile, and notification secrets remain sensitive and must stay out
  of logs, diffs, final answers, and docs.
- Agent Gateway/MCP must not gain credential or live-trading authority during
  cleanup.
- Preserved broker credentials remain encrypted and user-scoped.

## Test Strategy Mapping

- Route and OpenAPI cleanup:
  `.venv/bin/python -m pytest backend_api_python/tests/test_openapi.py -q`
- Backend health and Agent Gateway preservation:
  `.venv/bin/python -m pytest backend_api_python/tests/test_health.py backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py -q`
- Strategy/backtest preservation:
  `.venv/bin/python -m pytest backend_api_python/tests/test_backtest_execution.py -q`
- API artifact synchronization:
  `cd backend_api_python && ../.venv/bin/python scripts/export_openapi.py --output ../.codex/wiki/reference/api/openapi.generated.yaml && diff -u ../.codex/wiki/reference/api/openapi.yaml ../.codex/wiki/reference/api/openapi.generated.yaml; rm -f ../.codex/wiki/reference/api/openapi.generated.yaml`
- Wiki synchronization:
  `python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json`
  and `python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json`


## Closeout Evidence

Status: complete on 2026-06-01.

Implementation removed Docker/Railway/GHCR deployment assets, Community marketplace routes/services/schema, USDT payment workers/routes/settings/schema, and Billing/credits/VIP/membership code paths. README, AGENT, wiki pages, and OpenAPI artifacts now describe the local Gunicorn/nginx, PostgreSQL, Redis, no-paid-product baseline.

Validation evidence is recorded in `task-plans/4phases-checklist.md` and includes compileall, health/OpenAPI/Agent Gateway/backtest tests, OpenAPI export, residual scans, and wiki rebuild/doctor.
