---
description: API and behavior contracts for the local nginx slimdown scope.
---

# Contracts: Local Nginx Slimdown

## API Contracts

### Preserved Endpoint Families

- Auth, OAuth, Turnstile-backed login checks, user profile endpoints that do
  not expose credits/VIP.
- Credentials and broker configuration endpoints.
- IBKR, MT5, Alpaca, and other preserved broker route modules.
- Strategy, indicator, backtest, experiment, market data, portfolio, and
  notification endpoints.
- Agent Gateway under `backend_api_python/app/routes/agent_v1/`.
- Health and non-billing settings endpoints.

### Removed Endpoint Families

- Community marketplace endpoints from
  `backend_api_python/app/routes/community.py`.
- Billing endpoints from `backend_api_python/app/routes/billing.py`.
- USDT payment endpoints under `/api/billing/usdt/*` or equivalent billing
  route prefixes.
- Credits/VIP admin and user endpoints from user/settings routes.
- Membership purchase/order endpoints.

Removed endpoints must disappear from route registration and from
`.codex/wiki/reference/api/openapi.yaml`.

## Shared Types / Schema Definitions And Ownership

Preserved schema ownership:

- `backend_api_python/migrations/init.sql` remains the canonical first-boot
  PostgreSQL schema.
- User identity, auth, roles, OAuth, security logs, credentials, strategies,
  indicators, backtests, trades, portfolio, notification, Agent Gateway, and
  broker tables remain owned by the backend.

Removed schema ownership:

- Community purchase/comment/review tables and marketplace-only columns.
- `credits`, `vip_expires_at`, `vip_plan`, `vip_is_lifetime`, and
  `vip_monthly_credits_last_grant` user columns.
- Credit log, membership order, and USDT payment order tables.
- Billing/payment settings rows or defaults.

## Event / Worker Contracts

Preserved workers:

- Pending order worker, portfolio monitor, strategy runtime workers, and Agent
  Gateway async jobs, subject to existing configuration.

Removed workers:

- USDT order/payment watcher startup from `backend_api_python/app/__init__.py`.
- Any recurring membership/credit grant job.

## Validation Rules And Compatibility Policy

- Route removals must be reflected in OpenAPI artifacts and tests.
- Existing AI and analysis endpoints must no longer validate credits, VIP, or
  billing status before executing.
- Registration and OAuth signup must not grant credits or VIP state.
- Admin user APIs must not expose credit adjustment or credit log operations.
- Settings APIs must not emit billing, payment, membership, or USDT payment
  configuration.
- Trading symbols, including pairs containing `USDT`, remain valid where they
  are market symbols rather than payment workflow identifiers.

## Requirement Boundary Notes

- This scope removes external monetization for this checkout; it does not
  remove authentication, authorization, broker credential isolation, or
  notification security.
- This scope does not guarantee a downgrade migration for already-populated
  production databases unless a later implementation phase adds one explicitly.
- If preserved frontend source has stale calls to removed APIs, those calls are
  implementation blockers for the relevant phase.

## Security-Sensitive Fields And Redaction

Never expose the following in docs, tests, final answers, or generated wiki
content:

- OAuth secrets.
- Turnstile secrets.
- Email, SMS, and Telegram tokens.
- Broker API keys, OAuth tokens, cookies, and session credentials.
- LLM provider keys.
- Any historical USDT payment private keys or watcher credentials encountered
  during cleanup.


## Closeout Evidence

Status: complete on 2026-06-01.

Implementation removed Docker/Railway/GHCR deployment assets, Community marketplace routes/services/schema, USDT payment workers/routes/settings/schema, and Billing/credits/VIP/membership code paths. README, AGENT, wiki pages, and OpenAPI artifacts now describe the local Gunicorn/nginx, PostgreSQL, Redis, no-paid-product baseline.

Validation evidence is recorded in `task-plans/4phases-checklist.md` and includes compileall, health/OpenAPI/Agent Gateway/backtest tests, OpenAPI export, residual scans, and wiki rebuild/doctor.
