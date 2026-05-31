---
title: Product Architecture
type: concept
status: current
scope: quantdinger-core
last_checked: 2026-06-01
related_files:
  - path: backend_api_python/app/__init__.py
    role: owner
  - path: backend_api_python/app/routes
    role: caller
  - path: backend_api_python/app/services
    role: owner
  - path: backend_api_python/app/data_sources
    role: owner
  - path: backend_api_python/migrations/init.sql
    role: owner
  - path: backend_api_python/gunicorn_config.py
    role: config
code_anchors:
  - id: quantdinger-flask-app-factory
    kind: function
    file: backend_api_python/app/__init__.py
    symbol: create_app
    role: defines
  - id: quantdinger-runtime-workers
    kind: behavior
    file: backend_api_python/app/__init__.py
    symbol: start_pending_order_worker
    role: explains
  - id: quantdinger-first-boot-schema
    kind: schema
    file: backend_api_python/migrations/init.sql
    symbol: qd_agent_tokens
    role: references
source_docs:
  - README.md
  - backend_api_python/README.md
tags:
  - architecture
  - product
  - backend
updated: 2026-06-01T02:05:00+08:00
---

# Product Architecture

## Scope

QuantDinger is a self-hosted quant operating system. The product combines a
Flask backend, PostgreSQL state, Redis-backed caching and workers, local nginx,
direct exchange execution clients, an Agent Gateway, and an optional MCP server.

This checkout is intentionally local and non-paid-product oriented: no Docker
Compose, Dockerfiles, GHCR/Railway publishing, community marketplace, USDT
payment, credits, VIP, or membership purchase surfaces are active.

## Runtime Topology

The supported topology is:

- PostgreSQL: local or private-network database initialized from
  `backend_api_python/migrations/init.sql`.
- Redis: local or private-network cache and coordination service.
- Backend: Flask API on `127.0.0.1:5000`, started with `python run.py` or
  Gunicorn.
- nginx: browser-facing static/frontend and reverse proxy boundary.
- MCP: optional wrapper over the preserved Agent Gateway REST API.

Most backend, strategy, Agent Gateway, and MCP work should not require frontend
source.

## Current Code Anchors

- `backend_api_python/app/__init__.py`: Flask app construction, route
  registration, and startup workers.
- `backend_api_python/app/routes/`: browser and REST route modules.
- `backend_api_python/app/services/`: product behavior, strategy runtime,
  backtests, live trading, AI, notifications, user management, and workers.
- `backend_api_python/app/data_sources/`: normalized market data adapters,
  cache, circuit breaker, and rate-limit helpers.
- `backend_api_python/app/data_providers/`: higher-level provider feeds such
  as sentiment, heatmap, news, opportunities, and market families.
- `backend_api_python/app/utils/`: database, auth, credential crypto, safe
  execution, cache, market visibility, and runtime logs.
- `backend_api_python/migrations/init.sql`: canonical first-boot PostgreSQL
  schema.
- `mcp_server/`: optional MCP server over Agent Gateway.

## Backend Boundaries

The backend package is organized by responsibility:

- `app/routes`: HTTP surfaces for browser UI, agent API, auth, market data,
  backtests, strategies, quick trade, portfolio, settings, credentials, and
  broker-specific flows.
- `app/services`: business logic for backtests, experiments, strategy runtime,
  live trading, indicator workspace, fast analysis, LLM use, notifications,
  user management, and background workers.
- `app/data_sources`: market data providers for crypto, US stock, CN/HK,
  forex, futures, MOEX, Tencent, and related cache/rate-limit helpers.
- `app/utils`: database, auth, credential encryption, safe execution,
  multi-user broker sessions, logging, and data formatting.

The backend is the source of truth. The frontend and MCP server should remain
clients of backend contracts, not parallel implementations.

## Database Domains

The schema covers these durable product domains:

- users, auth, OAuth states, login attempts, security logs, roles, referral
  state, notification settings, and chart templates;
- market data, private indicators, strategies, strategy logs, positions, and
  trades;
- backtest runs, trades, equity points, experiments, optimization jobs, and AI
  analysis output;
- encrypted exchange credentials and broker-specific session state;
- Agent Gateway tokens, jobs, audit rows, and paper order records.

Runtime code may add missing compatibility columns with idempotent guards, but
new canonical schema should still be reflected in `migrations/init.sql`.

## Product Surfaces

Primary user-facing surfaces:

- Market dashboard, watchlists, technical indicators, and fast AI analysis.
- Private indicator IDE and strategy workspace.
- Backtest history, tuning, experiments, and AI optimization.
- Live bots, quick trade, portfolio, exchange credentials, and broker accounts.
- Agent token management and MCP/REST integration.
- Admin settings for branding, auth, notifications, runtime settings, and API
  keys.

Machine-facing surfaces:

- `/api/agent/v1`: scoped Agent Gateway for external agents and automation.
- `mcp_server/`: optional MCP wrapper over the Agent Gateway.
- `/api/health`: backend liveness for local runtime and operators.

## Operating Topologies

QuantDinger intentionally supports two deployment shapes:

- Self-hosted private stack: operator controls credentials, agent scopes, and
  whether live trading is enabled.
- Hosted or SaaS-style stack: multi-tenant controls should force paper-only
  agent behavior and reject trading-class agent tokens.

Keep this topology distinction visible in future docs and code. A self-hosted
operator can choose risk. A shared hosted system must fail closed around capital
movement and credential access.

## Change Rules

- Add backend behavior in services first; keep routes thin and request/response
  oriented.
- Keep `user_id` and tenant identity explicit in database queries, background
  jobs, strategy operations, agent calls, and broker sessions.
- Do not bypass `safe_exec.py` for generated indicators or strategy snippets.
- Treat `SECRET_KEY`, exchange keys, OAuth secrets, LLM keys, and notification
  credentials as production secrets.
- Do not reintroduce paid-product gates, marketplace workflow, payment workers,
  or container deployment scaffolding without an explicit new scope.
- Prefer idempotent startup guards for upgrade compatibility, but do not hide
  real migration requirements in unrelated request paths.
- Keep wiki pages as the durable manual. README and `AGENT.md` should summarize
  and link, not become competing long-form docs.

## Verification

Use the smallest relevant check for the changed surface:

```bash
curl -f http://127.0.0.1:5000/api/health
curl -f http://localhost/api/health
uv run python -m pytest backend_api_python/tests/test_health.py
```
