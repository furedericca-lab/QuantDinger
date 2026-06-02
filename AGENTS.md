# AGENTS.md

This is the repo-local operating contract for developers and coding agents in
`/root/code/QuantDinger`.

The host-level `AGENTS.md` still controls OpenClaw host safety, secrets,
service operations, DNS/proxy/mount behavior, and runtime guardrails. This file
adds QuantDinger project architecture, source boundaries, and development
workflow.

## 1. Source Of Truth

Use this precedence for implementation decisions:

1. current source code and runtime evidence;
2. current active scope docs under `.codex/scopes/<scope>/` when present;
3. current wiki pages under `.codex/wiki/`;
4. README and this file as entry points;
5. deleted legacy docs only through the wiki archive map, not as active files.

Primary entry points:

- `README.md`: operator-facing product and workflow guide.
- `AGENTS.md`: developer/agent-facing architecture and workflow contract.
- Archived scopes:
  - [.codex/scopes/archive/merge-upstream-v3-0-22/](.codex/scopes/archive/merge-upstream-v3-0-22/) preserves the completed upstream `v3.0.22` merge evidence.
  - `.codex/scopes/archive/local-nginx-slimdown/` preserves the local nginx/no-paid-product slimdown evidence after closeout.
- [.codex/wiki/index.md](.codex/wiki/index.md): structured project knowledge,
  decision log, and maintenance log.
- [Product Architecture](.codex/wiki/concepts/product-architecture.md):
  current product and runtime topology.
- [Strategy Backtest And Execution](.codex/wiki/implementation/strategy-backtest-and-execution.md):
  strategy runtime, backtest engine, signal semantics, and live boundary.
- [Agent Gateway And MCP](.codex/wiki/implementation/agent-gateway-and-mcp.md):
  machine API, scopes, audit, jobs, and MCP wrapper.
- [Deployment And Operations](.codex/wiki/implementation/deployment-and-operations.md):
  local Gunicorn/nginx runtime, ports, and operational checks.
- [Configuration And Integrations](.codex/wiki/reference/configuration-and-integrations.md):
  environment, OAuth, notifications, LLM, and local runtime settings.
- [Broker And Market Guides](.codex/wiki/reference/broker-and-market-guides.md):
  exchange, broker, market type, and data-source notes.
- [Project Governance](.codex/wiki/reference/project-governance.md):
  contribution, security, conduct, trademarks, and release guidance.
- [API Conventions](.codex/wiki/reference/api-conventions.md):
  human API, Agent Gateway, OpenAPI artifact paths, and contract rules.
- [Source Docs Archive Map](.codex/wiki/reference/source-docs-archive-map.md):
  mapping from deleted `docs/` and top-level governance files into wiki pages.
- [Upstream Merge Playbook](.codex/wiki/reference/upstream-merge-playbook.md):
  reusable release-merge triage rules for preserving the local nginx,
  no-paid-product, wiki-first, frontend-submodule baseline.

Do not treat the deleted legacy `docs/` tree as something to restore during
normal maintenance. If upstream adds genuinely useful durable documentation,
move the content into `.codex/wiki/` instead of reintroducing competing docs.

## 2. Architecture Map

Top-level ownership:

- `backend_api_python/`: Flask product backend, database access, strategy
  runtime, market data, live trading, Agent Gateway, and operational services.
- `backend_api_python/app/routes/`: browser/API route modules, including
  `/api/agent/v1`.
- `backend_api_python/app/services/`: business logic for strategies,
  backtests, experiments, AI, trading, notifications, users, and workers.
- `backend_api_python/app/data_sources/`: normalized market data adapters,
  cache, circuit breaker, rate limits, and symbol families.
- `backend_api_python/app/data_providers/`: higher-level market feeds such as
  sentiment, heatmaps, news, commodities, indices, and opportunities.
- `backend_api_python/app/utils/`: auth, agent auth, credential encryption,
  database access, safe execution, broker sessions, logging, and utility
  functions.
- `backend_api_python/migrations/init.sql`: canonical first-boot PostgreSQL
  schema.
- `mcp_server/`: `quantdinger-mcp`, an additive MCP wrapper over Agent Gateway
  REST APIs.
- `scripts/`: operational helper scripts.
- nginx: local reverse proxy and static/frontend serving boundary, configured
  outside this repo. On `openclaw`, the active vhost is
  `/etc/nginx/conf.d/quantdinger.conf`.
- systemd or another host process manager: local backend/Gunicorn service owner.
  On `openclaw`, the active unit is `quantdinger.service`.
- `.codex/wiki/`: current durable knowledge for this checkout.

The backend service layer is the source of truth. Frontend code and MCP tools
must remain clients of backend contracts, not parallel implementations.

## 3. Configuration And Runtime Rules

Canonical backend configuration is `backend_api_python/.env`, created from
`backend_api_python/env.example`.

Required first-start checks:

- `SECRET_KEY` is generated and not the default placeholder.
- `ADMIN_USER`, `ADMIN_PASSWORD`, and `ADMIN_EMAIL` are intentional.
- `FRONTEND_URL` matches the user-facing origin.
- `DATABASE_URL` and Redis settings point to local or private services.
- `ENABLE_PENDING_ORDER_WORKER`, `ENABLE_PORTFOLIO_MONITOR`, and
  `DISABLE_RESTORE_RUNNING_STRATEGIES` are intentional.
- `ALLOW_LOCAL_DESKTOP_BROKERS` is false for public SaaS deployments unless a
  private bridge to IBKR/MT5 is explicitly supported.
- `QUANTDINGER_DEPLOYMENT_MODE=saas` or `hosted` is used for shared hosted
  deployments that must force Agent Gateway trading to paper-only behavior.

Current `openclaw` public single-user baseline:

- Public hostname is `https://tsw.momoe.qzz.io` through the existing
  Cloudflare Tunnel. This historical hostname is intentional for the current
  local baseline; do not rename local nginx or `FRONTEND_URL` unless the
  Cloudflare public hostname is changed first.
- `quantdinger.service` runs Gunicorn from `backend_api_python/` and binds to
  `127.0.0.1:5000`.
- Frontend source is tracked as the `frontend/` git submodule, pointing at
  `https://github.com/furedericca-lab/QuantDinger-Vue`. nginx serves the
  browser WebUI from `/var/www/quantdinger` and proxies `/api/*` to
  `127.0.0.1:5000`. The deployed static files are built from `frontend/dist`
  at the pinned frontend commit.
- `backend_api_python/.env` should keep `ENABLE_REGISTRATION=false`,
  `PYTHON_API_HOST=127.0.0.1`, `FRONTEND_URL=https://tsw.momoe.qzz.io`,
  `OPENAPI_ENABLED=false`, and `AGENT_LIVE_TRADING_ENABLED=false`.
- The retired TSW services must remain absent/inactive:
  `tsw-gravity-api.service`, `tsw-gravity-worker.service`, and
  `/var/www/tsw-webui`.
- Cloudflare Access is a remote account policy, not something local file edits
  can expand. Unless a live Cloudflare check proves otherwise, treat the
  current QuantDinger exposure as app-JWT-protected behind a Tunnel-only local
  origin, with registration disabled.
- Current observed Cloudflare behavior redirects unauthenticated public
  requests for `/`, `/login`, `/assets/*`, and `/api/health` to Cloudflare
  Access. Use loopback Host/SNI checks for local WebUI validation, and use a
  real Access-authenticated browser session for public end-to-end validation.
- If Cloudflare changes are explicitly authorized later, prefer protecting the
  whole `tsw.momoe.qzz.io` hostname instead of only a legacy path.

Hard rules:

- Do not rotate `SECRET_KEY` casually. It signs JWTs and derives credential
  encryption material.
- Do not commit `.env`, exchange keys, OAuth secrets, LLM keys, notification
  tokens, cookies, or private credentials.
- Keep PostgreSQL and Redis loopback-bound unless the deployment explicitly
  uses a private network boundary.
- Keep runtime config changes reflected in the wiki when they alter operator
  behavior.

## 4. Auth, Users, And Credentials

Key files:

- `backend_api_python/app/utils/auth.py`
- `backend_api_python/app/routes/auth.py`
- `backend_api_python/app/services/oauth_service.py`
- `backend_api_python/app/utils/credential_crypto.py`
- `backend_api_python/app/routes/credentials.py`
- `backend_api_python/app/utils/broker_session.py`
- `backend_api_python/migrations/init.sql`

Rules:

- Browser JWT sessions and agent tokens are separate identity systems.
- Multi-user behavior must keep `user_id` and broker session isolation intact.
- Credential values must stay encrypted at rest and redacted from logs,
  responses, docs, tests, and final answers.
- OAuth redirect allowlists must be based on configured origins, not arbitrary
  request input.
- Security-sensitive denial paths should be explicit and auditable.

When editing this area, run focused auth/security tests or at least targeted
syntax/import checks and route-level smoke tests.

## 5. Strategy And Indicator Layer

Key files:

- `backend_api_python/app/routes/indicator.py`
- `backend_api_python/app/routes/strategy.py`
- `backend_api_python/app/services/indicator_workspace.py`
- `backend_api_python/app/services/indicator_default_template.py`
- `backend_api_python/app/services/indicator_params.py`
- `backend_api_python/app/services/strategy.py`
- `backend_api_python/app/services/strategy_compiler.py`
- `backend_api_python/app/services/strategy_lifecycle.py`
- `backend_api_python/app/services/strategy_script_runtime.py`
- `backend_api_python/app/utils/safe_exec.py`

Current strategy forms:

- `IndicatorStrategy`: dataframe-oriented indicator and backtest signal code.
- `ScriptStrategy`: event-driven `on_init` / `on_bar` scripts using a runtime
  context object.
- Cross-sectional strategies: multi-symbol ranking and allocation workflows.

Signal rules:

- Prefer explicit four-way signals for complex strategies:
  `open_long`, `close_long`, `open_short`, `close_short`.
- Two-way `buy` / `sell` is acceptable for simpler strategies only when
  `tradeDirection` is clear.
- Do not mix two-way and four-way signal columns as competing fill drivers.
- Generated Python code must pass safe execution validation before save or
  execution.

Sandbox rules:

- Do not allow imports, file/network access, process execution, reflection
  escapes, dunder traversal, dangerous pandas/NumPy I/O, or host access from
  user strategy code.
- Do not weaken `safe_exec.py` to make generated code pass. Fix the generated
  code or add a narrow reviewed API surface.

## 6. Backtest And Experiment Layer

Key files:

- `backend_api_python/app/routes/backtest.py`
- `backend_api_python/app/routes/experiment.py`
- `backend_api_python/app/services/backtest.py`
- `backend_api_python/app/services/backtest_execution.py`
- `backend_api_python/app/services/backtest_presets.py`
- `backend_api_python/app/services/experiment/`
- `backend_api_python/app/utils/agent_jobs.py`

Current behavior:

- `BacktestService` owns the in-process backtest engine.
- The engine fetches data, runs sandboxed strategy/indicator code, normalizes
  signals, simulates fills/fees/slippage/liquidation/end exits, and persists
  runs, trades, and equity points.
- The current engine version is `strategy-backtest-v1`.
- Strict mode maps to closed-bar signal confirmation and next-bar-open fills.
- Crypto high-precision backtests can select `1m`, `5m`, `15m`, or `30m`
  execution timeframes when requested ranges stay within workload caps.

When changing backtests:

- preserve persisted run/trade/equity compatibility;
- keep engine-version and config snapshots useful for later diagnosis;
- test strict-mode and non-strict behavior when fill semantics change;
- check Agent Gateway async job behavior if backtest APIs are exposed there.

## 7. Live Trading Boundary

Key files:

- `backend_api_python/app/services/trading_executor.py`
- `backend_api_python/app/services/pending_order_worker.py`
- `backend_api_python/app/services/exchange_execution.py`
- `backend_api_python/app/services/live_trading/`
- `backend_api_python/app/routes/quick_trade.py`
- `backend_api_python/app/routes/portfolio.py`
- broker routes under `app/routes/alpaca.py`, `ibkr.py`, and `mt5.py`

Current boundary:

- `TradingExecutor` is a signal provider. It starts strategy threads, fetches
  price/K-line inputs, evaluates code, deduplicates signals, and writes
  pending orders.
- `PendingOrderWorker` is the dispatch boundary. It polls pending orders,
  sends notifications for signal mode, and dispatches live execution through
  `app.services.live_trading` when live mode is enabled.
- `app.services.live_trading` contains direct REST clients. It is the live
  order submission layer.
- CCXT is for public market data, charting, and backtest inputs. It is not the
  live order submission layer.

Rules:

- Do not run real-money trading in tests or agent sessions unless the user
  explicitly authorizes that boundary.
- Hosted or multi-tenant deployments must force agent trading to paper-only and
  reject trading-scope token issuance.
- Spot close sizing must respect free base balance, lot filters, and safety
  ratio settings.
- Swap/futures behavior must respect reduce-only, position side, and
  exchange-specific symbol notation.
- Position sync must respect cache/backoff settings to avoid exchange bans.

## 8. Agent Gateway And MCP

Key files:

- `backend_api_python/app/routes/agent_v1/`
- `backend_api_python/app/utils/agent_auth.py`
- `backend_api_python/app/utils/agent_jobs.py`
- `mcp_server/src/quantdinger_mcp/server.py`
- `mcp_server/README.md`

Capability classes:

- `R`: read market data, strategies, jobs, portfolio, and health.
- `W`: write workspace resources such as indicators or stopped strategies.
- `B`: run backtests, regime detection, experiments, and tuning jobs.
- `N`: notifications and low-risk side effects.
- `C`: credentials. Denied by default and admin-only.
- `T`: trading and capital movement. Denied by default and paper-only by
  default.

Rules:

- Agent Gateway routes live under `/api/agent/v1`.
- Identity is exclusively agent-token based, never browser JWT based.
- Every call, including denial paths, should write `qd_agent_audit`.
- Tokens are prefixed and hashed at rest.
- Scope, market, and instrument allowlists must be enforced server-side.
- Async jobs should use `qd_agent_jobs` and expose polling/SSE where relevant.
- MCP wraps only capabilities already protected by REST.
- MCP must not expose live trading unless the product is explicitly redesigned.

## 9. Brokers And Market Data

Key files:

- `backend_api_python/app/data_sources/`
- `backend_api_python/app/services/live_trading/`
- `backend_api_python/app/services/ibkr_trading/`
- `backend_api_python/app/services/mt5_trading/`
- `backend_api_python/app/services/alpaca_trading/`
- `backend_api_python/app/services/broker_market_policy.py`
- `backend_api_python/app/utils/local_brokers.py`

Rules:

- Market type matters. Spot, swap, futures, forex, equities, and broker-backed
  symbols use different notation and execution assumptions.
- IBKR and MT5 require reachable local desktop or gateway software; disable
  local desktop brokers on public SaaS deployments unless explicitly bridged.
- Alpaca paper/live mode must be explicit.
- Public market data failures should be diagnosed separately from private
  broker order failures.
- Proxy settings such as `PROXY_URL` may be required when exchange REST access fails from the backend process.

## 10. Notifications And Runtime Settings

Key files:

- `backend_api_python/app/services/email_service.py`
- `backend_api_python/app/services/signal_notifier.py`
- `backend_api_python/app/routes/settings.py`
- `backend_api_python/env.example`

Rules:

- Notification credentials must stay in environment or encrypted settings.
- Strategy code should request notification behavior through product settings,
  not embed raw tokens.
- Runtime settings must not reintroduce paid-product gates, payment processors,
  credits, VIP, memberships, or marketplace controls.
- Settings changes that alter operator behavior belong in `.codex/wiki/`.

## 11. Documentation And Wiki Policy

The old `docs/` markdown tree and top-level governance files were consolidated
into `.codex/wiki/`.

Rules:

- Do not reintroduce long-form `docs/` files unless the user explicitly asks or
  a clear product need exists.
- Do not recreate `docs/api/`, `docs/agent/`, or `docs/API_CONVENTIONS.md`.
  API artifacts and API contract documentation live at:
  `.codex/wiki/reference/api/openapi.yaml`,
  `.codex/wiki/reference/api/index.html`,
  `.codex/wiki/reference/agent/agent-openapi.json`, and
  `.codex/wiki/reference/api-conventions.md`.
- `backend_api_python/scripts/export_openapi.py` must keep its default output
  pointed at `.codex/wiki/reference/api/openapi.yaml`.
- OpenAPI CI, PR templates, README, and wiki verification commands must point
  at the wiki API artifact paths, not old `docs/` paths.
- Repo-task-driven scope docs belong under `.codex/scopes/<scope>/`.
- Completed scope archives belong under `.codex/scopes/archive/<scope>/`.
- Durable behavior, architecture, and operating assumptions belong in
  `.codex/wiki/`.
- README should remain an operator entry point.
- AGENTS should remain a developer/agent contract.
- Do not store secrets, tokens, private keys, cookies, or raw credentials in
  README, wiki, tests, examples, or final answers.

After wiki changes:

```bash
python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json
python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json
```

For code-to-wiki navigation, use `wiki.py nav search`, `wiki.py nav goto`, and
`wiki.py nav refs` before loading broad docs or editing high-risk modules.

## 12. Upstream Merge Preservation

This checkout has intentionally diverged from upstream in its documentation
and local-runtime baseline. Future merges must preserve the local base unless
the user explicitly asks to restore upstream behavior.

During upstream merge, rebase, or cherry-pick work:

- Treat `.codex/wiki/` as the durable documentation surface.
- If upstream adds or changes useful Markdown under `docs/`, extract the useful
  facts into the relevant wiki page and update
  `.codex/wiki/reference/source-docs-archive-map.md`.
- Do not accept upstream changes that restore `docs/api/openapi.yaml`,
  `docs/api/index.html`, `docs/agent/agent-openapi.json`, or
  `docs/API_CONVENTIONS.md`; keep those paths under `.codex/wiki/reference/`.
- Keep `.github/workflows/openapi-ci.yml`, `.github/PULL_REQUEST_TEMPLATE.md`,
  README, AGENTS, and `backend_api_python/scripts/export_openapi.py` aligned
  with the wiki API paths after conflict resolution.
- Do not restore upstream Docker Compose, Dockerfile, GHCR, Railway, payment,
  membership, credits, VIP, or marketplace scaffolding just because a merge
  marks it as added. Preserve the local deletion when the local wiki or runtime
  model already absorbed the useful content.
- If upstream adds useful deployment or monetization documentation, extract only
  the non-sensitive durable facts into `.codex/wiki/` and keep the local
  nginx/no-paid-product baseline intact unless the user explicitly changes it.

Post-merge minimum checks:

```bash
rg -n "docs/api|docs/agent|docs/API_CONVENTIONS|API_CONVENTIONS" README.md AGENTS.md .github backend_api_python .codex/wiki -S
python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json
python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json
cd backend_api_python && python scripts/export_openapi.py
```

The `rg` check should only return this preservation section and unrelated
third-party URLs, if any. It must not reveal active README, CI, code, or wiki
links that still point at old local `docs/` API artifact paths. The OpenAPI
export must write to `.codex/wiki/reference/api/openapi.yaml`.

## 13. Validation Defaults

Use the narrowest meaningful check first.

Local Python environment:

```bash
uv sync
```

General backend:

```bash
uv run python -m pytest backend_api_python/tests/test_health.py
uv run python -m py_compile <changed-file.py>
```

Agent Gateway:

```bash
uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py
```

Backtest and trading semantics:

```bash
uv run python -m pytest backend_api_python/tests/test_backtest_execution.py backend_api_python/tests/test_trading_execution_modes.py
```

Local runtime work:

```bash
curl -f http://127.0.0.1:5000/api/health
curl -fk https://tsw.momoe.qzz.io/api/health
curl -fkI --resolve tsw.momoe.qzz.io:443:127.0.0.1 https://tsw.momoe.qzz.io/assets/index-DBOji-Sz.js
curl -k -sS -o /dev/null -w '%{http_code}\n' --resolve tsw.momoe.qzz.io:443:192.168.1.153 https://tsw.momoe.qzz.io/api/health
```

Do not claim completion for high-risk changes without either running the
focused checks or clearly stating why validation could not be run.

## 14. High-Risk Areas

Treat these paths as security-sensitive:

- `backend_api_python/app/utils/auth.py`
- `backend_api_python/app/utils/agent_auth.py`
- `backend_api_python/app/routes/agent_v1/`
- `backend_api_python/app/utils/credential_crypto.py`
- `backend_api_python/app/utils/safe_exec.py`
- `backend_api_python/app/services/live_trading/`
- `backend_api_python/app/services/pending_order_worker.py`
- `backend_api_python/app/services/trading_executor.py`
- `backend_api_python/migrations/init.sql`
- `mcp_server/src/quantdinger_mcp/server.py`

For these paths, prefer focused tests plus manual review of denial paths,
redaction behavior, user isolation, and runtime configuration impact.
