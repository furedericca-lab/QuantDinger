---
title: Deployment And Operations
type: implementation
status: current
scope: quantdinger-deploy
last_checked: 2026-06-01
related_files:
  - path: backend_api_python/env.example
    role: config
  - path: backend_api_python/run.py
    role: owner
  - path: backend_api_python/gunicorn_config.py
    role: config
  - path: backend_api_python/app/config/settings.py
    role: owner
  - path: README.md
    role: doc
  - path: AGENT.md
    role: doc
code_anchors:
  - id: quantdinger-backend-env-template
    kind: config
    file: backend_api_python/env.example
    symbol: SECRET_KEY
    role: references
  - id: quantdinger-backend-run-entrypoint
    kind: module
    file: backend_api_python/run.py
    symbol: app
    role: explains
  - id: quantdinger-gunicorn-config
    kind: config
    file: backend_api_python/gunicorn_config.py
    symbol: bind
    role: defines
source_docs:
  - README.md
  - AGENT.md
tags:
  - deployment
  - operations
  - nginx
updated: 2026-06-01T02:05:00+08:00
---

# Deployment And Operations

## Scope

The supported runtime for this checkout is local PostgreSQL, local Redis,
Gunicorn or `python run.py` for the Flask backend, and nginx as the reverse
proxy/static frontend boundary.

Docker Compose, Dockerfiles, GHCR publishing, Railway config, community
marketplace, billing, USDT payment, credits, VIP, and membership purchase
surfaces have been removed. Future upstream syncs should not restore them unless
the user explicitly changes the product baseline.

## First Start

1. Copy `backend_api_python/env.example` to `backend_api_python/.env`.
2. Replace `SECRET_KEY` with a random value of at least 32 bytes.
3. Review `ADMIN_USER`, `ADMIN_PASSWORD`, `ADMIN_EMAIL`, `FRONTEND_URL`,
   database, Redis, LLM provider, broker, notification, and live-trading toggles.
4. Start PostgreSQL and Redis with the host service manager.
5. Start the backend with `uv run --directory backend_api_python python run.py`
   for local development or `gunicorn -c gunicorn_config.py run:app` for a
   production-style process.
6. Configure nginx to serve the frontend and proxy `/api/` plus
   `/api/agent/v1` to `127.0.0.1:5000`.

The backend refuses unsafe default `SECRET_KEY` values in normal deployment.
Do not rotate `SECRET_KEY` casually because it also derives the Fernet key used
for encrypted exchange credentials.

## Ports

Defaults:

- nginx/WebUI: `http://localhost`.
- Backend direct: `127.0.0.1:5000`.
- PostgreSQL: `127.0.0.1:5432`.
- Redis: `127.0.0.1:6379`.

Keep PostgreSQL and Redis bound to loopback or an explicit private network. Do
not expose database or cache ports publicly.

## Backend Startup Behavior

The backend loads `backend_api_python/.env`, applies proxy env via `PROXY_URL`,
and may auto-apply `migrations/init.sql` unless `SKIP_AUTO_MIGRATE=true`.

Important worker toggles:

- `ENABLE_PENDING_ORDER_WORKER`: pending-order dispatch loop.
- `ENABLE_PORTFOLIO_MONITOR`: portfolio monitor loop.
- `DISABLE_RESTORE_RUNNING_STRATEGIES`: prevent automatic strategy restore.
- `GUNICORN_WORKERS` / `GUNICORN_THREADS`: backend concurrency.
- `DB_POOL_MIN` / `DB_POOL_MAX`: database connection pool.

Keep route-level executor workers well below `DB_POOL_MAX`, because each worker
can need a database connection.

## nginx Boundary

Recommended local production shape:

- nginx owns the browser-facing origin.
- frontend/static files are served by nginx.
- `/api/*` proxies to backend port `5000`.
- `FRONTEND_URL` matches the browser-facing origin.
- HTTPS is used when the origin is not strictly local.

Production-sensitive settings:

- Set `QUANTDINGER_DEPLOYMENT_MODE=saas` or `hosted` for shared deployments.
- Set `ALLOW_LOCAL_DESKTOP_BROKERS=false` when IBKR/MT5 local desktop software
  is not intentionally reachable.
- Keep `AGENT_LIVE_TRADING_ENABLED=false` unless agent live trading is
  deliberately designed and reviewed.
- Set `PROXY_URL` when backend exchange access requires a proxy.

## Common Operations

```bash
uv sync
uv run --directory backend_api_python python run.py
cd backend_api_python && gunicorn -c gunicorn_config.py run:app
curl -f http://127.0.0.1:5000/api/health
curl -f http://localhost/api/health
```

## Troubleshooting

- Backend cannot start: check `backend_api_python/.env`, `SECRET_KEY`, database
  connectivity, Redis connectivity, and backend logs.
- nginx 502/504: check backend health, proxy target, and service logs.
- Exchange symbol errors: verify market type, venue symbol format, and whether
  the exchange uses spot, swap, or broker-specific notation.
- `connection pool exhausted`: lower executor/worker concurrency or increase
  `DB_POOL_MAX` and PostgreSQL `max_connections` together.
- Market data fails from the backend: set `PROXY_URL` and verify certificate
  behavior from the backend process.
- OAuth invalid redirect: check `FRONTEND_URL`, `OAUTH_ALLOWED_REDIRECTS`, and
  provider callback URLs.
- Agent token unexpectedly rejected: check hosted mode, scopes, token status,
  expiry, market/instrument allowlists, and rate limits.

## Closeout Checks

For deployment or runtime changes, report what was checked:

```bash
curl -f http://127.0.0.1:5000/api/health
curl -f http://localhost/api/health
python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json
python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json
```
