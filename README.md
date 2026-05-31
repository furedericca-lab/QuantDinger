# QuantDinger

`QuantDinger` is a self-hosted AI quant operating system. It combines market
data, indicator authoring, Python strategy runtimes, server-side backtests,
live trading adapters, multi-user administration, an Agent Gateway, and an MCP
server.

The system is a quant operations console, not a broker shortcut. Use it to
prepare configuration, inspect markets, author indicators, run simulations,
review strategy evidence, and verify safety gates before any paper or live
execution path is used.

This checkout keeps durable project knowledge in `.codex/wiki/`. README is the
operator-facing usage guide. Detailed architecture, integration, governance,
and verification notes live in the wiki.

## Access

- Local WebUI: `http://localhost:8888`
- Backend health: `http://localhost:5000/api/health`
- Backend API: `http://localhost:5000`
- Agent Gateway: `http://localhost:8888/api/agent/v1`
- Human Web API OpenAPI: `.codex/wiki/reference/api/openapi.yaml`
- Agent Gateway OpenAPI: `.codex/wiki/reference/agent/agent-openapi.json`

The default Docker stack serves the frontend through a prebuilt Vue/Nginx image
and builds the backend from local source. PostgreSQL and Redis are bound to
loopback by default and should not be exposed publicly.

## What You Use It For

Use the system for these jobs:

1. **Prepare deployment config**: create `backend_api_python/.env`, generate a
   strong `SECRET_KEY`, set admin credentials, and confirm deployment mode.
2. **Inspect markets**: search symbols, open K-line charts, review watchlists,
   indicators, dashboard data, and fast analysis output.
3. **Author indicators**: write or generate Python indicator code, validate it
   through the sandbox, and save reusable indicator definitions.
4. **Create strategies**: build indicator-backed strategies, event-driven
   script strategies, grid/runtime templates, or cross-sectional workflows.
5. **Run backtests**: simulate strategy behavior across symbols, timeframes,
   fees, slippage, strict mode, and high-precision crypto execution windows.
6. **Tune and experiment**: run regime detection, structured tuning,
   experiment pipelines, and AI-assisted optimization when configured.
7. **Operate trading flows**: use signal, paper, or explicitly enabled live
   execution paths through the backend worker model.
8. **Connect brokers**: configure crypto exchanges, IBKR, MT5, and Alpaca with
   the correct market type and deployment assumptions.
9. **Expose agent access**: issue scoped Agent Gateway tokens and optionally
   run `quantdinger-mcp` for MCP-compatible AI clients.
10. **Administer the product**: manage users, branding, OAuth, notifications,
    billing, USDT payments, roles, and runtime settings.

Agent access is not a replacement for operator review. Credential and trading
authority stay denied by default and must be intentionally scoped.

## Recommended Workflow

### 1. Confirm configuration is safe

Create `backend_api_python/.env`.

```bash
cp backend_api_python/env.example backend_api_python/.env
python3 - <<'PY'
from pathlib import Path
import secrets
p = Path("backend_api_python/.env")
text = p.read_text()
text = text.replace(
    "SECRET_KEY=quantdinger-secret-key-change-me",
    "SECRET_KEY=" + secrets.token_hex(32),
)
p.write_text(text)
PY
```

Check:

- `SECRET_KEY` is generated and not the default placeholder;
- `ADMIN_USER`, `ADMIN_PASSWORD`, and `ADMIN_EMAIL` are intentional;
- `FRONTEND_URL` matches the user-facing origin;
- database and Redis settings match the runtime;
- live trading, local desktop brokers, OAuth, notifications, billing, LLM, and
  Agent Gateway settings are intentional.

Do not rotate `SECRET_KEY` casually. It signs JWTs and derives the Fernet key
used for encrypted exchange credentials.

### 2. Start the stack

Run:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
docker compose logs --tail=100 backend
curl -f http://localhost:5000/api/health
```

Open `http://localhost:8888`, sign in with the configured admin account, and
change default credentials before real use.

The default runtime contains:

- `postgres`: PostgreSQL 16 initialized from
  `backend_api_python/migrations/init.sql`;
- `redis`: cache and worker coordination;
- `backend`: Flask API on container port `5000`;
- `frontend`: prebuilt Vue/Nginx image on port `8888`.

### 3. Verify market and broker assumptions

Before strategy work, confirm the selected market, symbol format, and exchange
or broker path.

Check:

- crypto market type is `spot` or `swap` as intended;
- exchange symbol notation matches the selected venue;
- IBKR or MT5 is reachable only when a local desktop/gateway bridge exists;
- Alpaca paper/live mode is explicit;
- `PROXY_URL` is configured inside Docker when exchange REST access needs a
  proxy.

Market-data availability does not prove live-order readiness.

### 4. Author and validate strategy assets

Use the web app or Agent Gateway to create indicators and strategies.

Important strategy forms:

- `IndicatorStrategy`: dataframe-oriented indicator and backtest signal code.
- `ScriptStrategy`: event-driven `on_init` / `on_bar` scripts.
- Cross-sectional strategies: multi-symbol ranking and allocation workflows.

Generated code must pass `safe_exec.py` sandbox validation before save or
execution. Do not weaken the sandbox to make generated code pass.

### 5. Backtest before execution

Run a backtest before starting bots.

Use backtests to inspect:

- signal interpretation;
- fees, slippage, and fill assumptions;
- strict-mode versus non-strict behavior;
- crypto execution precision tier;
- persisted trades, equity curve, and result metrics.

Backtest evidence is simulation evidence. It is not proof that a broker account
is configured, funded, reachable, or safe for live order submission.

### 6. Start signal, paper, or live paths deliberately

`TradingExecutor` evaluates strategy signals and writes pending orders.
`PendingOrderWorker` is the dispatch boundary. Direct REST clients under
`app.services.live_trading` submit live orders only when live mode is
explicitly enabled and configured.

CCXT is for public market data, charting, and backtest inputs. It is not the
live order submission layer.

Hosted or multi-tenant deployments should reject trading-scope agent tokens and
force paper-only behavior.

### 7. Connect agents only after scoping

Issue an agent token in the product, then run MCP if needed:

```bash
QUANTDINGER_BASE_URL=http://localhost:8888 \
QUANTDINGER_AGENT_TOKEN=qd_agent_xxxxx \
uvx quantdinger-mcp
```

Use read/workspace/backtest scopes for ordinary AI clients. Do not expose
credential or live-trading authority through MCP.

## Page Reference

### Market And Analysis

Purpose:

- market search and symbol inspection;
- K-line, indicator, watchlist, and dashboard views;
- fast analysis and AI-assisted summaries when an LLM provider is configured.

Use this page family to decide whether a symbol and timeframe deserve strategy
work. Do not use analysis output as execution authority.

### Indicator Workspace

Purpose:

- Python indicator authoring;
- sandbox validation;
- reusable indicator definitions;
- typed parameters for strategies and backtests.

Use this surface when you need to create or revise signal-generating code.
Indicator code should be deterministic dataframe logic, not a place for
credentials, network calls, or filesystem access.

### Strategies

Purpose:

- stopped strategy creation and editing;
- strategy parameter normalization;
- script-strategy runtime configuration;
- lifecycle controls before signal/paper/live operation.

Use this page family after indicator validation and before backtests or live
workers. Keep strategy identity and `user_id` isolation intact.

### Backtests And Experiments

Purpose:

- backtest submission and history;
- trade/equity/result inspection;
- strict-mode and high-precision crypto simulation;
- regime detection, tuning, experiment pipelines, and AI optimization.

Use this surface to build evidence before execution. Do not treat a profitable
backtest as broker readiness.

### Live Trading And Portfolio

Purpose:

- signal, paper, and explicitly enabled live execution modes;
- pending-order dispatch;
- position sync;
- portfolio and local trade records.

Use this surface only after broker credentials, market type, sizing, and
execution mode are clear. Real account actions require explicit operator
intent.

### Broker Accounts

Purpose:

- crypto exchange credential configuration;
- IBKR, MT5, and Alpaca connection setup;
- account, position, and broker-specific state inspection.

Important distinction:

- crypto exchange execution uses direct REST clients;
- IBKR and MT5 require reachable local gateway/terminal software;
- Alpaca paper/live behavior must be configured explicitly.

### Agent Gateway

Purpose:

- scoped machine access at `/api/agent/v1`;
- token-based identity separate from browser JWT sessions;
- audited read, workspace, backtest, notification, credential, and trading
  capability classes;
- async jobs with polling or SSE streaming.

Capability classes are `R`, `W`, `B`, `N`, `C`, and `T`. New agent tokens
should not receive credential or trading scope by default.

API references:

- Human Web API OpenAPI: `.codex/wiki/reference/api/openapi.yaml`
- Human Web API ReDoc viewer: `.codex/wiki/reference/api/index.html`
- API conventions: `.codex/wiki/reference/api-conventions.md`
- Agent Gateway OpenAPI: `.codex/wiki/reference/agent/agent-openapi.json`

### MCP Server

Purpose:

- MCP-compatible wrapper over approved Agent Gateway REST capabilities;
- desktop or remote AI-client integration;
- bounded job polling/streaming helpers.

MCP is additive. REST remains the source of truth. MCP intentionally does not
wrap live trading.

### Admin Settings

Purpose:

- branding and legal text;
- OAuth and registration controls;
- notification channels;
- billing and USDT payment settings;
- deployment and safety toggles.

Use this surface when runtime behavior changes. Keep secrets out of docs, logs,
examples, and prompts.

## Concepts In Plain English

QuantDinger separates research, simulation, and execution.

The strategy path is:

- indicator or script code produces signals;
- backtests simulate those signals with explicit assumptions;
- `TradingExecutor` produces pending order intent;
- `PendingOrderWorker` dispatches signal, paper, or live behavior;
- direct REST clients handle live exchange order submission.

Prefer explicit four-way signals for complex strategies:

- `open_long`
- `close_long`
- `open_short`
- `close_short`

Two-way `buy` / `sell` remains valid for simpler strategies when
`tradeDirection` is clear.

## Local Development For Operators

Install Python dependencies in a repo-local `.venv`:

```bash
uv sync
```

Start the backend:

```bash
uv run --directory backend_api_python python run.py
```

Routine backend rebuild:

```bash
docker compose up -d --build backend
```

Frontend source is not required for normal backend development. Clone a sibling
`./QuantDinger-Vue/` checkout only when intentionally working on local frontend
source with `docker-compose.build.yml`.

## Verification

Use [Current Verification Commands](.codex/wiki/reference/current-verification-commands.md)
for the current command families.

Common checks:

```bash
uv run python -m pytest backend_api_python/tests/test_health.py
uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py
uv run python -m pytest backend_api_python/tests/test_backtest_execution.py backend_api_python/tests/test_trading_execution_modes.py
uv run python -m pytest backend_api_python/tests/test_usdt_payment_idempotency.py
```

Runtime checks:

```bash
docker compose config
docker compose ps
docker compose logs --tail=100 backend
curl -f http://localhost:5000/api/health
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

The previous long-form `docs/` markdown set and top-level governance files were
consolidated into `.codex/wiki/`. Add durable documentation there first.

## Safety Boundaries

- Do not put exchange, LLM, OAuth, notification, payment, cookie, or private
  credential values in README, wiki, tests, examples, logs, or prompts.
- Do not expose PostgreSQL or Redis publicly.
- Do not weaken `safe_exec.py` for generated strategy code.
- Do not run live trading or payment actions against real accounts unless that
  boundary is explicitly authorized.
- Do not expose credential or live-trading authority through MCP.
- Keep hosted or multi-tenant agent tokens paper-only by default.

Live execution details are in
[Strategy Backtest And Execution](.codex/wiki/implementation/strategy-backtest-and-execution.md).
