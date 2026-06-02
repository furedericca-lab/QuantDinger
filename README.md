# QuantDinger

`QuantDinger` is a self-hosted AI quant operating system. It combines market
data, indicator authoring, Python strategy runtimes, server-side backtests,
live trading adapters, multi-user administration, an Agent Gateway, and an MCP
server.

This checkout is optimized for a local backend plus nginx deployment. It does
not ship Docker Compose, GHCR/Railway deployment assets, community marketplace,
USDT payment, credits, VIP, or membership purchase flows.

Durable project knowledge lives in `.codex/wiki/`. README is the operator-facing
entry point; architecture, integration, governance, and verification details
live in the wiki.

## Access

- Public WebUI on `openclaw`: `https://tsw.momoe.qzz.io`
- Public access is gated by Cloudflare Access for the full hostname before
  nginx or QuantDinger receive traffic.
- Local WebUI through nginx: `https://tsw.momoe.qzz.io` with Host/SNI resolved
  to loopback for origin checks.
- Backend health direct: `http://127.0.0.1:5000/api/health`
- Backend API direct: `http://127.0.0.1:5000`
- Agent Gateway through nginx: `https://tsw.momoe.qzz.io/api/agent/v1`
- Human Web API OpenAPI: `.codex/wiki/reference/api/openapi.yaml`
- Agent Gateway OpenAPI: `.codex/wiki/reference/agent/agent-openapi.json`

The deployed WebUI on `openclaw` is served from `/var/www/quantdinger`. Its
static artifact was extracted from
`ghcr.io/brokermr810/quantdinger-frontend:v3.0.22`; the Vue source is not part
of this checkout.

## What You Use It For

1. Prepare `backend_api_python/.env`, generate a strong `SECRET_KEY`, and set
   the first admin account.
2. Inspect markets, symbols, K-lines, watchlists, indicators, dashboard data,
   and fast analysis output.
3. Author private Python indicators, validate them through the sandbox, and save
   reusable indicator definitions.
4. Create indicator-backed, script, grid/runtime, or cross-sectional strategies.
5. Run backtests and experiments before any paper or live execution path.
6. Operate signal, paper, or explicitly enabled live trading flows.
7. Configure crypto exchanges, IBKR, MT5, and Alpaca with explicit market type
   and runtime assumptions.
8. Issue scoped Agent Gateway tokens and optionally run `quantdinger-mcp` for
   MCP-compatible AI clients.
9. Administer users, branding, OAuth, notifications, roles, runtime settings,
   and API keys.

Agent access is not a replacement for operator review. Credential and trading
authority stay denied by default and must be intentionally scoped.

## Recommended Workflow

### 1. Configure The Backend

```bash
cp backend_api_python/env.example backend_api_python/.env
python3 - <<'PY2'
from pathlib import Path
import secrets
p = Path("backend_api_python/.env")
text = p.read_text()
text = text.replace(
    "SECRET_KEY=quantdinger-secret-key-change-me",
    "SECRET_KEY=" + secrets.token_hex(32),
)
p.write_text(text)
PY2
```

Check:

- `SECRET_KEY` is generated and not the placeholder.
- `ADMIN_USER`, `ADMIN_PASSWORD`, and `ADMIN_EMAIL` are intentional.
- `FRONTEND_URL` matches the nginx/WebUI origin.
- PostgreSQL and Redis settings point to local or explicitly private services.
- live trading, local desktop brokers, OAuth, notifications, LLM, and Agent
  Gateway settings are intentional.

Do not rotate `SECRET_KEY` casually. It signs JWTs and derives the Fernet key
used for encrypted exchange credentials.

### 2. Start Local Services

Install dependencies:

```bash
uv sync
```

Start PostgreSQL and Redis with your host service manager, then run the backend:

```bash
uv run --directory backend_api_python python run.py
```

Production-style backend process:

```bash
cd backend_api_python
gunicorn -c gunicorn_config.py run:app
```

nginx should serve the frontend build and reverse proxy `/api/` and
`/api/agent/v1` to the backend on `127.0.0.1:5000`. On `openclaw`, the active
vhost is `/etc/nginx/conf.d/quantdinger.conf` and the public hostname remains
`https://tsw.momoe.qzz.io`.

Check:

```bash
curl -f http://127.0.0.1:5000/api/health
curl -f http://localhost/api/health
curl -fkI --resolve tsw.momoe.qzz.io:443:127.0.0.1 https://tsw.momoe.qzz.io/assets/index-DBOji-Sz.js
curl -k -sSI https://tsw.momoe.qzz.io/api/health | sed -n '1,8p'
```

### 3. Verify Market And Broker Assumptions

Before strategy work, confirm the selected market, symbol format, and exchange
or broker path.

- crypto market type is `spot` or `swap` as intended;
- exchange symbol notation matches the selected venue;
- IBKR or MT5 is reachable only when a local desktop/gateway bridge exists;
- Alpaca paper/live mode is explicit;
- `PROXY_URL` is configured when exchange REST access needs a proxy.

Market-data availability does not prove live-order readiness.

### 4. Author And Validate Strategy Assets

Use the web app or Agent Gateway to create indicators and strategies.

- `IndicatorStrategy`: dataframe-oriented indicator and backtest signal code.
- `ScriptStrategy`: event-driven `on_init` / `on_bar` scripts.
- Cross-sectional strategies: multi-symbol ranking and allocation workflows.

Generated code must pass `safe_exec.py` sandbox validation before save or
execution. Do not weaken the sandbox to make generated code pass.

### 5. Backtest Before Execution

Use backtests to inspect signal interpretation, fees, slippage, fill
assumptions, strict mode, crypto precision windows, persisted trades, equity
curve, and result metrics. Backtest evidence is simulation evidence; it is not
proof that a broker account is configured, funded, reachable, or safe for live
order submission.

### 6. Start Signal, Paper, Or Live Paths Deliberately

`TradingExecutor` evaluates strategy signals and writes pending orders.
`PendingOrderWorker` is the dispatch boundary. Direct REST clients under
`app.services.live_trading` submit live orders only when live mode is explicitly
enabled and configured.

Hosted or multi-tenant deployments should reject trading-scope agent tokens and
force paper-only behavior.

### 7. Connect Agents Only After Scoping

```bash
QUANTDINGER_BASE_URL=http://localhost QUANTDINGER_AGENT_TOKEN=qd_agent_xxxxx uvx quantdinger-mcp
```

Use read/workspace/backtest scopes for ordinary AI clients. Do not expose
credential or live-trading authority through MCP.

## Page Reference

- **Market And Analysis**: market search, K-lines, watchlists, dashboard data,
  and fast analysis.
- **Indicator Workspace**: private Python indicator authoring, sandbox
  validation, reusable definitions, and typed parameters.
- **Strategies**: stopped strategy creation/editing, parameter normalization,
  script runtime config, and lifecycle controls.
- **Backtests And Experiments**: backtest submission/history, trade/equity
  inspection, strict mode, tuning, and AI optimization.
- **Live Trading And Portfolio**: signal, paper, explicitly enabled live
  execution, pending order dispatch, position sync, and local trade records.
- **Broker Accounts**: crypto exchange, IBKR, MT5, and Alpaca setup.
- **Agent Gateway**: scoped machine access at `/api/agent/v1`.
- **MCP Server**: MCP-compatible wrapper over approved Agent Gateway REST
  capabilities.
- **Admin Settings**: branding, OAuth, registration, notifications, runtime
  settings, and API keys.

## Verification

Use [Current Verification Commands](.codex/wiki/reference/current-verification-commands.md)
for the current command families.

Common checks:

```bash
uv run python -m pytest backend_api_python/tests/test_health.py
uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py
uv run python -m pytest backend_api_python/tests/test_backtest_execution.py backend_api_python/tests/test_trading_execution_modes.py
cd backend_api_python && SKIP_STARTUP_HOOKS=1 OPENAPI_ENABLED=false ../.venv/bin/python scripts/export_openapi.py --output ../.codex/wiki/reference/api/openapi.generated.yaml
```

Runtime checks:

```bash
curl -f http://127.0.0.1:5000/api/health
curl -f http://localhost/api/health
```

## Active Work And Knowledge

Knowledge entry points:

- [Project Wiki Index](.codex/wiki/index.md)
- [Product Architecture](.codex/wiki/concepts/product-architecture.md)
- [Strategy Backtest And Execution](.codex/wiki/implementation/strategy-backtest-and-execution.md)
- [Agent Gateway And MCP](.codex/wiki/implementation/agent-gateway-and-mcp.md)
- [Deployment And Operations](.codex/wiki/implementation/deployment-and-operations.md)
- [Configuration And Integrations](.codex/wiki/reference/configuration-and-integrations.md)
- [Broker And Market Guides](.codex/wiki/reference/broker-and-market-guides.md)
- [Project Governance](.codex/wiki/reference/project-governance.md)
- [Source Docs Archive Map](.codex/wiki/reference/source-docs-archive-map.md)

Completed scope archives:

- [.codex/scopes/archive/merge-upstream-v3-0-22/](.codex/scopes/archive/merge-upstream-v3-0-22/)
- `.codex/scopes/archive/local-nginx-slimdown/` after closeout

## Safety Boundaries

- Do not put exchange, LLM, OAuth, notification, cookie, or private credential
  values in README, wiki, tests, examples, logs, or prompts.
- Do not expose PostgreSQL or Redis publicly.
- Do not weaken `safe_exec.py` for generated strategy code.
- Do not run live trading against real accounts unless that boundary is
  explicitly authorized.
- Do not expose credential or live-trading authority through MCP.
- Keep hosted or multi-tenant agent tokens paper-only by default.

Live execution details are in
[Strategy Backtest And Execution](.codex/wiki/implementation/strategy-backtest-and-execution.md).
