---
title: Deployment And Operations
type: implementation
status: current
scope: quantdinger-deploy
last_checked: 2026-05-31
related_files:
  - docker-compose.yml
  - docker-compose.ghcr.yml
  - docker-compose.build.yml
  - backend_api_python/env.example
  - backend_api_python/Dockerfile
  - backend_api_python/run.py
source_docs:
  - docs/CLOUD_DEPLOYMENT_EN.md
  - docs/CLOUD_DEPLOYMENT_CN.md
  - DEVELOPMENT.md
  - docs/multi-user-setup.md
tags:
  - deployment
  - operations
  - docker
updated: 2026-05-31T15:35:00+08:00
---

# Deployment And Operations

## Scope

Docker Compose is the default deployment path. The main stack starts
PostgreSQL, Redis, the Flask backend, and a prebuilt Vue frontend image.

This page owns first-start behavior, image topology, runtime checks, and the
operator boundary between local development, self-hosted production, and
hosted/SaaS-style deployments.

## First Start

1. Copy `backend_api_python/env.example` to `backend_api_python/.env`.
2. Replace `SECRET_KEY` with a random value of at least 32 bytes.
3. Review `ADMIN_USER`, `ADMIN_PASSWORD`, `FRONTEND_URL`, database settings,
   LLM provider settings, and live trading toggles.
4. Start the stack with `docker compose up -d`.

The backend refuses unsafe default `SECRET_KEY` values in normal deployment.
Do not rotate `SECRET_KEY` casually because it also derives the Fernet key used
for encrypted exchange credentials.

First-start proof:

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=100 backend
curl -f http://localhost:5000/api/health
```

## Frontend Model

The default frontend is a prebuilt image from GHCR. Use
`docker-compose.build.yml` only when hacking on a local `./QuantDinger-Vue/`
checkout. Routine backend development does not require Node.js or frontend
source.

Image tag knobs:

- `FRONTEND_IMAGE`: override the frontend image path.
- `FRONTEND_TAG`: override only the frontend tag.
- `IMAGE_TAG`: shared image tag knob where supported.
- `IMAGE_PREFIX`: base-image mirror prefix for common Docker Hub images.
- `BUILD_REGION`: backend Dockerfile source selection, with `cn` defaulting to
  Aliyun mirrors with fallback and `global` using official sources directly.

## Ports

Defaults:

- Frontend: `8888`.
- Backend: `127.0.0.1:5000`.
- PostgreSQL: `127.0.0.1:5432`.
- Redis: `127.0.0.1:6379`.

Keep PostgreSQL and Redis bound to loopback unless an explicit private network
deployment requires otherwise. Do not expose database ports publicly.

Compose exposes `BACKEND_PORT`, `FRONTEND_PORT`, `DB_PORT`, and `REDIS_PORT`
as override knobs. Keep database/cache overrides private-network scoped.

## Backend Startup Behavior

The backend loads `/app/.env`, receives Compose-provided database/cache values,
and starts with Gunicorn settings from env. Startup may auto-apply
`migrations/init.sql` unless `SKIP_AUTO_MIGRATE=true`.

Important worker toggles:

- `ENABLE_PENDING_ORDER_WORKER`: pending-order dispatch loop.
- `ENABLE_PORTFOLIO_MONITOR`: portfolio monitor loop.
- `DISABLE_RESTORE_RUNNING_STRATEGIES`: prevent automatic strategy restore.
- `GUNICORN_WORKERS` / `GUNICORN_THREADS`: backend concurrency.
- `DB_POOL_MIN` / `DB_POOL_MAX`: database connection pool.

Keep route-level executor workers well below `DB_POOL_MAX`, because each
worker can need a database connection.

## Production Reverse Proxy

Recommended production shape:

- Public HTTPS terminates at Nginx or a cloud load balancer.
- Frontend and API share one public domain where possible.
- `/api/*` proxies to backend port `5000`.
- Static frontend traffic proxies to the frontend container.
- Configure `FRONTEND_URL` to the user-facing HTTPS origin.

Production-sensitive settings:

- Use HTTPS for public origins.
- Set `QUANTDINGER_DEPLOYMENT_MODE=saas` or `hosted` for shared deployments.
- Set `ALLOW_LOCAL_DESKTOP_BROKERS=false` when IBKR/MT5 local desktop
  software is not intentionally reachable.
- Keep `AGENT_LIVE_TRADING_ENABLED=false` unless agent live trading is
  deliberately designed and reviewed.
- Keep `PROXY_URL` explicit inside Docker when exchange access requires a
  proxy; host browser/VPN success does not prove container egress.

## Common Operations

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose pull
docker compose up -d
docker compose up -d --build backend
```

For slow Docker pulls, set `IMAGE_PREFIX` in the project-root `.env` or
configure Docker Engine registry mirrors.

Backend-only local development:

```bash
uv sync
uv run --directory backend_api_python python run.py
```

Routine backend rebuild:

```bash
docker compose up -d --build backend
```

## Troubleshooting

- Backend cannot start: check `backend_api_python/.env`, `SECRET_KEY`,
  database connectivity, and backend logs.
- Frontend `host not found in upstream "backend"`: ensure all Compose services
  are on the same project network and backend container exists.
- Nginx 502/504: check backend health, proxy target, and container logs.
- Exchange symbol errors: verify market type, venue symbol format, and whether
  the exchange uses spot, swap, or broker-specific notation.
- `connection pool exhausted`: lower executor/worker concurrency or increase
  `DB_POOL_MAX` and PostgreSQL `PG_MAX_CONNECTIONS` together.
- Binance/Coinbase market data fails inside Docker: set `PROXY_URL` for the
  backend container and verify certificate behavior.
- OAuth invalid redirect: check `FRONTEND_URL`, `OAUTH_ALLOWED_REDIRECTS`, and
  provider callback URLs.
- Agent token unexpectedly rejected: check hosted mode, scopes, token status,
  expiry, market/instrument allowlists, and rate limits.

## Closeout Checks

For deployment or runtime changes, report what was checked:

```bash
docker compose config
docker compose ps
curl -f http://localhost:5000/api/health
docker compose logs --tail=100 backend
```

If the frontend image, reverse proxy, or public origin changed, also verify the
browser-facing origin and `/api/*` proxy path.
