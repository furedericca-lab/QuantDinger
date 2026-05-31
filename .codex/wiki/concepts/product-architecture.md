---
title: Product Architecture
type: concept
status: current
scope: quantdinger-core
last_checked: 2026-05-31
related_files:
  - backend_api_python/app/__init__.py
  - backend_api_python/app/routes
  - backend_api_python/app/services
  - backend_api_python/app/data_sources
  - docker-compose.yml
source_docs:
  - README.md
  - backend_api_python/README.md
  - docs/README_CN.md
  - docs/README_JA.md
  - docs/README_KO.md
  - docs/README_TH.md
  - docs/README_VI.md
  - docs/README_AR.md
tags:
  - architecture
  - product
  - backend
updated: 2026-05-31T15:20:00+08:00
---

# Product Architecture

## Scope

QuantDinger is a self-hosted quant operating system. The product combines a
Flask backend, PostgreSQL state, Redis-backed caching and workers, a prebuilt
Vue frontend image, direct exchange execution clients, an Agent Gateway, and an
optional MCP server.

It is not only a strategy research repo. It has login, roles, branding,
billing toggles, OAuth, notification channels, encrypted broker credentials,
multi-user data isolation, strategy execution workers, and a machine-facing
API. Architecture changes should therefore be evaluated as product changes,
not just as isolated Python edits.

## Runtime Topology

The default Docker stack is:

- `postgres`: PostgreSQL 16 with `backend_api_python/migrations/init.sql`.
- `redis`: Redis 7 for cache and worker coordination.
- `backend`: Flask API on port `5000`, with env loaded from
  `backend_api_python/.env`.
- `frontend`: prebuilt Nginx/Vue image on port `8888`, proxying API calls to
  the backend.

The Compose backend is built from local source. The frontend is pulled from a
prebuilt GHCR image unless `docker-compose.build.yml` is layered in with a
sibling `./QuantDinger-Vue/` checkout. Most backend, strategy, Agent Gateway,
and MCP work should not require frontend source.

## Current Code Anchors

- `backend_api_python/app/__init__.py`: Flask app construction and route
  registration.
- `backend_api_python/app/routes/`: browser and REST route modules.
- `backend_api_python/app/services/`: product behavior, strategy runtime,
  backtests, live trading, AI, notifications, billing, and workers.
- `backend_api_python/app/data_sources/`: normalized market data adapters,
  cache, circuit breaker, and rate-limit helpers.
- `backend_api_python/app/data_providers/`: higher-level provider feeds such
  as sentiment, heatmap, news, opportunities, and market families.
- `backend_api_python/app/utils/`: database, auth, credential crypto, safe
  execution, cache, market visibility, and runtime logs.
- `backend_api_python/migrations/init.sql`: canonical first-boot PostgreSQL
  schema.
- `docker-compose.yml`: default local product runtime.

## Backend Boundaries

The backend package is organized by responsibility:

- `app/routes`: HTTP surfaces for browser UI, agent API, auth, market data,
  backtests, strategies, quick trade, portfolio, settings, credentials,
  billing, and broker-specific flows.
- `app/services`: business logic for backtests, experiments, strategy runtime,
  live trading, indicator workspace, fast analysis, LLM use, notifications,
  billing, user management, and background workers.
- `app/data_sources`: market data providers for crypto, US stock, CN/HK,
  forex, futures, MOEX, Tencent, and related cache/rate-limit helpers.
- `app/utils`: database, auth, credential encryption, safe execution,
  multi-user broker sessions, logging, and data formatting.

The backend is the source of truth. The frontend and MCP server should remain
clients of backend contracts, not parallel implementations.

## Database Domains

The schema covers these durable product domains:

- users, auth, OAuth states, login attempts, security logs, roles, credits,
  VIP state, and referral state;
- market data, indicators, strategies, strategy logs, positions, and trades;
- backtest runs, trades, equity points, experiments, optimization jobs, and AI
  analysis output;
- encrypted exchange credentials and broker-specific session state;
- Agent Gateway tokens, jobs, audit rows, and paper order records;
- billing, membership orders, and USDT payment reconciliation.

Runtime code may add missing compatibility columns with idempotent guards, but
new canonical schema should still be reflected in `migrations/init.sql`.

## Product Surfaces

Primary user-facing surfaces:

- Market dashboard, watchlists, technical indicators, and fast AI analysis.
- Indicator IDE and strategy workspace.
- Backtest history, tuning, experiments, and AI optimization.
- Live bots, quick trade, portfolio, exchange credentials, and broker accounts.
- Agent token management and MCP/REST integration.
- Admin settings for branding, auth, notifications, billing, and deployment.

Machine-facing surfaces:

- `/api/agent/v1`: scoped Agent Gateway for external agents and automation.
- `mcp_server/`: optional MCP wrapper over the Agent Gateway.
- `/api/health`: backend liveness for Compose and operators.

## Operating Topologies

QuantDinger intentionally supports two deployment shapes:

- Self-hosted private stack: operator controls credentials, agent scopes, and
  whether live trading is enabled.
- Hosted or SaaS-style stack: multi-tenant controls should force paper-only
  agent behavior and reject trading-class agent tokens.

Keep this topology distinction visible in future docs and code. A self-hosted
operator can choose risk. A shared hosted system must fail closed around
capital movement and credential access.

## Current Product Bias

QuantDinger is more productized than a research repo: login, billing toggles,
OAuth, notifications, broker configuration, Agent Gateway, MCP, Docker Compose,
and prebuilt frontend images are all part of the operating model. This makes it
a good base for secondary development, but it also means feature work should
respect multi-user isolation, deployment configuration, and live-trading safety
instead of adding local-only shortcuts.

## Change Rules

- Add backend behavior in services first; keep routes thin and
  request/response oriented.
- Keep `user_id` and tenant identity explicit in database queries, background
  jobs, strategy operations, agent calls, and broker sessions.
- Do not bypass `safe_exec.py` for generated indicators or strategy snippets.
- Treat `SECRET_KEY`, exchange keys, OAuth secrets, LLM keys, USDT watcher
  keys, and notification credentials as production secrets.
- Prefer idempotent startup guards for upgrade compatibility, but do not hide
  real migration requirements in unrelated request paths.
- Keep wiki pages as the durable manual. README and `AGENT.md` should
  summarize and link, not become competing long-form docs.

## Verification

Use the smallest relevant check for the changed surface:

```bash
docker compose config
docker compose ps
docker compose logs --tail=100 backend
curl -f http://localhost:5000/api/health
cd backend_api_python && pytest tests/test_health.py
```
