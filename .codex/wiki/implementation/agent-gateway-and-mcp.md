---
title: Agent Gateway And MCP
type: implementation
status: current
scope: quantdinger-agent-api
last_checked: 2026-06-01
related_files:
  - path: backend_api_python/app/routes/agent_v1
    role: owner
  - path: backend_api_python/app/routes/agent_v1/__init__.py
    role: owner
  - path: backend_api_python/app/routes/agent_v1/me_tokens.py
    role: owner
  - path: backend_api_python/app/services/agent_token_service.py
    role: owner
  - path: backend_api_python/app/utils/agent_auth.py
    role: owner
  - path: backend_api_python/app/utils/agent_jobs.py
    role: owner
  - path: backend_api_python/app/openapi
    role: owner
  - path: .codex/wiki/reference/agent/agent-openapi.json
    role: generated
  - path: backend_api_python/app/routes/agent_v1/quick_trade.py
    role: caller
  - path: mcp_server/src/quantdinger_mcp/server.py
    role: owner
code_anchors:
  - id: agent-gateway-blueprint-registration
    kind: function
    file: backend_api_python/app/routes/agent_v1/__init__.py
    symbol: register
    role: defines
  - id: agent-token-auth-scope-guard
    kind: decorator
    file: backend_api_python/app/utils/agent_auth.py
    symbol: agent_required
    role: defines
  - id: agent-self-token-management
    kind: route
    file: backend_api_python/app/routes/agent_v1/me_tokens.py
    symbol: bp
    role: defines
  - id: agent-token-service-issue-revoke
    kind: service
    file: backend_api_python/app/services/agent_token_service.py
    symbol: AgentTokenService
    role: defines
  - id: agent-idempotent-job-submission
    kind: decorator
    file: backend_api_python/app/utils/agent_auth.py
    symbol: with_idempotency
    role: defines
  - id: agent-quick-trade-capital-boundary
    kind: route
    file: backend_api_python/app/routes/agent_v1/quick_trade.py
    symbol: place_order
    role: explains
  - id: quantdinger-mcp-rest-wrapper
    kind: module
    file: mcp_server/src/quantdinger_mcp/server.py
    symbol: submit_backtest
    role: explains
  - id: agent-openapi-spec-artifact
    kind: schema
    file: .codex/wiki/reference/agent/agent-openapi.json
    symbol: Agent Gateway OpenAPI
    role: references
source_docs:
  - .codex/wiki/reference/agent/agent-openapi.json
  - mcp_server/README.md
tags:
  - agent
  - mcp
  - automation
  - safety
updated: 2026-06-01T00:42:00+08:00
---

# Agent Gateway And MCP

## Scope

QuantDinger exposes an Agent Gateway under `/api/agent/v1`. The gateway is for
external AI agents, coding assistants, MCP clients, and automation workflows
that need stable, scoped access to product behavior.

The gateway must stay thin. It adds identity, scopes, audit, rate limits,
idempotency, and async job handling while reusing the same service layer as the
browser product.

## Code Anchors

- Gateway routes are registered from `backend_api_python/app/routes/agent_v1/`.
- Authentication, scope checks, rate limits, idempotency, and audit helpers live
  in `backend_api_python/app/utils/agent_auth.py`.
- Async job persistence and polling helpers live in
  `backend_api_python/app/utils/agent_jobs.py`.
- MCP tools live under `mcp_server/` and should only wrap capabilities already
  exposed through REST.

Current route modules:

- `health.py`: public liveness and token-aware identity checks.
- `markets.py`: market list, symbol search, K-lines, and prices.
- `strategies.py`: scoped strategy listing, fetch, create, and update.
- `indicators.py`: indicator contract, code validation, save/list/get.
- `backtests.py`: backtest submission and related result access.
- `experiments.py`: regime detection, experiment pipelines, structured tuning,
  and AI optimization.
- `portfolio.py`: portfolio and paper-order reads.
- `quick_trade.py`: trading-class and paper-order boundary.
- `jobs.py`: async job polling and SSE streaming.
- `admin.py`: admin token issuance/revocation and audit visibility.
- `me_tokens.py`: authenticated user self-service token listing, issuance, and
  revocation through the Agent Gateway boundary.

`backend_api_python/app/services/agent_token_service.py` is the shared token
service for admin and self-service token operations. Keep token generation,
hashing, scope defaults, hosted-mode restrictions, and audit behavior there
rather than duplicating token logic in route modules.

## Capability Classes

Every agent endpoint and MCP tool should map to one risk class:

- `R`: read market data, symbols, strategies, jobs, portfolio, or health.
- `W`: write workspace resources such as indicators or stopped strategies.
- `B`: run backtests, regime detection, experiments, or tuning jobs.
- `N`: notifications and miscellaneous low-risk side effects.
- `C`: credentials. Denied by default and admin-only.
- `T`: trading and capital movement. Denied by default, paper-only by default,
  and requires explicit operator opt-in.

New agent tokens must not acquire `C` or `T` by default.

Suggested defaults:

- indicator authoring assistant: `R,W,B`;
- market or research assistant: `R,B`;
- read-only dashboard assistant: `R`;
- notification automation: `R,N`;
- credential or live trading automation: only after explicit operator review
  of deployment mode, token allowlists, paper-only behavior, and audit impact.

## Identity

Agent tokens belong to a tenant/user. Tokens are prefixed and hashed at rest.
JWT browser sessions are not valid for `/api/agent/v1`, and agent tokens are
not browser sessions.

Every agent call, including denial paths, should append an audit record to
`qd_agent_audit`.

Identity and authorization checks should include token hash lookup, status,
expiry, per-minute rate limit, scope class, market allowlist, instrument
allowlist, paper-only flag, hosted-mode guard, and idempotency where mutation
or async submission needs replay safety.

## Async Jobs

Backtests and experiment pipelines submit work to `qd_agent_jobs`. Clients poll
`/api/agent/v1/jobs/{id}` or subscribe to `GET /api/agent/v1/jobs/{id}/stream`.

The SSE stream uses event types such as `snapshot`, `progress`, `ping`, and
`result`. Long-running runners can opt in to live progress by accepting an
`on_progress` callback. The job helper detects the callback, pipes updates to
live SSE subscribers, and persists the latest snapshot for later polling.

Job runners should store enough request/result context for debugging without
persisting credentials or large raw payloads.

## Hosted Mode Guard

In hosted, SaaS, shared, or multi-tenant deployment mode, token issuance should
reject trading scope and force `paper_only=true`. This protects shared
deployments from accidental live trading through external agents even if other
flags are misconfigured.

Current defense-in-depth anchors:

- `QUANTDINGER_DEPLOYMENT_MODE=saas` or `hosted`: force hosted behavior.
- `AGENT_LIVE_TRADING_ENABLED=false`: hard kill switch for agent live trading.
- token `paper_only=true`: token-level capital-movement protection.

## MCP Layer

The MCP server is an additive wrapper over `/api/agent/v1`; REST remains the
source of truth. The MCP package exposes read, workspace, and backtest tools,
but intentionally does not wrap live trading.

The MCP layer must not request credentials from the model. It forwards the
operator-issued agent token and relies on server-side scopes and allowlists.

`QUANTDINGER_MCP_TRANSPORT` selects transport mode:

- `stdio`: default for desktop IDE clients.
- `sse`: server-sent events transport.
- `streamable-http`: remote IDE or cloud-agent transport. Bind with
  `QUANTDINGER_MCP_HOST` and `QUANTDINGER_MCP_PORT`.

Add new MCP tools only after the underlying capability is exposed and protected
through REST.

## OpenAPI Artifacts

The Agent Gateway keeps its machine-readable contract in
`.codex/wiki/reference/agent/agent-openapi.json`. Human Web API OpenAPI lives
under `.codex/wiki/reference/api/` and is generated from the flask-smorest
registration layer.

These files are wiki-owned generated API artifacts. If their semantics change,
update the API tests and this wiki page rather than relying on README links
alone.

MCP safety rules:

- never wrap credential reads or secret values;
- never expose admin JWT flows;
- keep quick-trade/live execution out of MCP unless explicitly redesigned;
- preserve payload limits for indicator source;
- keep long-running stream/poll helpers bounded by event and time caps;
- redact known credential fields from responses.

## Admin UI

The Vue admin surface issues and revokes agent tokens and displays audit logs.
When frontend source is present, the expected route is `/agent-tokens`, gated to
admin users. The API client should call the Agent Gateway rather than bypassing
its token, scope, and audit model.

## Verification

```bash
uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py
uv run python -m pytest backend_api_python/tests/test_openapi.py
uv run python -m py_compile backend_api_python/app/routes/agent_v1/__init__.py
uv run python -m py_compile backend_api_python/app/routes/agent_v1/me_tokens.py
uv run python -m py_compile backend_api_python/app/services/agent_token_service.py
uv run python -m py_compile backend_api_python/app/utils/agent_auth.py
uv run python -m py_compile backend_api_python/app/utils/agent_jobs.py
uv run python -m py_compile mcp_server/src/quantdinger_mcp/server.py
```
