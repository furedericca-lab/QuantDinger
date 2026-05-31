# QuantDinger Python API (backend)

Flask backend for QuantDinger: market data, indicators, AI analysis,
backtesting, strategy runtime, multi-user auth, broker adapters, notifications,
and Agent Gateway.

This backend is run locally from source. The supported deployment shape for this
checkout is Gunicorn or `python run.py` behind a local nginx reverse proxy. The
backend no longer owns Docker, Railway, GHCR, billing, USDT payment, credits,
VIP, membership, or community marketplace surfaces.

## Project Layout

```text
backend_api_python/
├─ app/
│  ├─ __init__.py                 # Flask app factory + startup hooks
│  ├─ config/                     # Settings (env-driven)
│  ├─ data_sources/               # Data sources + factory
│  ├─ routes/                     # REST endpoints
│  ├─ services/                   # Analysis, agents, strategies, search, users
│  └─ utils/                      # PostgreSQL helpers, auth, crypto, logging
├─ migrations/init.sql            # PostgreSQL schema initialization
├─ env.example                    # Copy to .env for local config
├─ requirements.txt
├─ run.py                         # Entrypoint
├─ gunicorn_config.py             # Production process config
└─ README.md
```

## Quick Start

### 1. Configure Environment

```bash
cp backend_api_python/env.example backend_api_python/.env
bash scripts/generate-secret-key.sh
```

Set at least:

```env
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=quantdinger
POSTGRES_USER=quantdinger
POSTGRES_PASSWORD=your_secure_password
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
ADMIN_USER=admin
ADMIN_PASSWORD=your_admin_password
ADMIN_EMAIL=admin@example.com
FRONTEND_URL=http://localhost
```

### 2. Install And Start

From the repo root:

```bash
uv sync
uv run --directory backend_api_python python run.py
```

Production-style process:

```bash
cd backend_api_python
gunicorn -c gunicorn_config.py run:app
```

nginx should serve frontend/static files and proxy API traffic to
`127.0.0.1:5000`.

### 3. Verify

```bash
curl -f http://127.0.0.1:5000/api/health
uv run python -m pytest backend_api_python/tests/test_health.py
```

## Notes

- `migrations/init.sql` is idempotently applied during backend startup.
- `SKIP_STARTUP_HOOKS=1` disables workers for OpenAPI export and CI.
- `PROXY_URL` controls backend outbound exchange/market-data egress when needed.
- Broker credentials and LLM/OAuth/notification secrets must stay in `.env` or
  encrypted storage, never docs or logs.
