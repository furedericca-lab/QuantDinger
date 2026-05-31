---
description: Milestones for slimming QuantDinger to a local nginx deployment and removing external monetization features.
---

# Scope Milestones: Local Nginx Slimdown

## In-Scope

- Remove Docker Compose, Dockerfile, GHCR, Railway, and container-first install
  assets that are unnecessary for host-local backend/Gunicorn plus nginx.
- Rewrite README, AGENT, and wiki deployment guidance for local nginx reverse
  proxy operation.
- Preserve Agent Gateway and `mcp_server/`.
- Preserve IBKR, MT5, Alpaca, OAuth, Turnstile, email, SMS, and Telegram.
- Remove Community marketplace behavior and its purchase/comment/review schema.
- Remove USDT payment and membership purchase behavior.
- Deep remove Billing, credits, and VIP fields, endpoints, service calls, admin
  tools, settings, schema, docs, and API contract references.

## Out-Of-Scope

- Removing broker integrations, exchange market data, or trading pairs that
  contain `USDT` as a market symbol.
- Removing OAuth, Turnstile, email, SMS, or Telegram notification support.
- Rewriting strategy/backtest/experiment/Agent Gateway architecture beyond the
  call-site changes needed to remove paid gates.
- Reintroducing the deleted `docs/` tree; durable docs stay under
  `.codex/wiki/`.
- Running live trades or changing external broker/account state.

## Decision Log

- MCP is preserved because the user identified it as useful for external agent
  integration and it wraps Agent Gateway REST rather than monetization.
- Broker integrations are preserved because IBKR, MT5, and Alpaca are local
  deployment requirements.
- OAuth, Turnstile, email, SMS, and Telegram are preserved pending future
  instructions.
- Community marketplace is removed because it is a business/marketplace surface
  and depends on paid purchase semantics.
- Billing, credits, VIP, membership, and USDT payment are removed deeply because
  the user does not need external paid functionality and explicitly rejected a
  waiting period for Phase 4.

## Milestones With Acceptance Gates

### Milestone 1: Local Nginx Deployment Baseline

Acceptance gate:

- Docker/Railway/GHCR assets are removed or rewritten out of active paths.
- README, AGENT, and wiki describe backend/Gunicorn plus nginx reverse proxy as
  the current local deployment baseline.
- MCP, Agent Gateway, broker, OAuth, Turnstile, and notification references are
  intact.
- OpenAPI and backend health tests still pass.

### Milestone 2: Community Marketplace Removal

Acceptance gate:

- Community marketplace routes/services are unregistered and removed.
- Marketplace purchase/comment/review schema and docs are removed without
  deleting core indicator workspace tables or strategy functionality.
- OpenAPI no longer exposes Community marketplace endpoints.
- Residual scans contain no active marketplace product language.

### Milestone 3: USDT Payment And Membership Purchase Removal

Acceptance gate:

- USDT payment services, watchers, startup worker, env/settings, schema, and
  billing subroutes are removed.
- Trading and market-data `USDT` symbol support remains intact.
- OpenAPI and tests no longer refer to payment USDT behavior.

### Milestone 4: Billing, Credits, And VIP Deep Removal

Acceptance gate:

- Billing service and route modules are removed from active imports and OpenAPI.
- User credits/VIP fields, credit logs, membership orders, registration bonuses,
  admin credit endpoints, billing settings, AI consumption/refund checks, and
  insufficient-credit errors are removed.
- AI, indicator, strategy, fast analysis, and portfolio monitor flows run
  without billing gates.
- README, AGENT, wiki, env example, schema, and tests contain no active
  Billing/credits/VIP product contract.

## Dependencies Across Milestones

- Milestone 1 can run independently and should run first to settle operator
  documentation before large feature deletion.
- Milestone 2 can run after Milestone 1 and before Billing removal because it
  has direct purchase/billing dependencies.
- Milestone 3 should run before Milestone 4 so payment watcher and membership
  purchase code is separated from broader credits/VIP removal.
- Milestone 4 depends on Milestones 2 and 3 to avoid leaving partial paid
  feature endpoints or orphaned purchase flows.

## Exit Criteria Per Milestone

- Each milestone updates `task-plans/4phases-checklist.md` with evidence,
  blocker status, and checkpoint confirmation.
- Each milestone runs focused tests plus `git diff --check`.
- Milestones that touch docs or wiki run wiki rebuild and doctor.
- Milestones that change routes run OpenAPI export diff and spectral lint.

## Escalation Triggers

- A planned deletion is found to be required by preserved broker, OAuth,
  Turnstile, notification, Agent Gateway, or MCP behavior.
- Existing database state requires a destructive data migration outside
  `backend_api_python/migrations/init.sql`.
- OpenAPI generation or import startup cannot succeed without redesigning
  preserved core strategy/backtest/auth modules.
- A frontend client cannot be updated because the relevant source is not
  present in this checkout.


## Closeout Evidence

Status: complete on 2026-06-01.

Implementation removed Docker/Railway/GHCR deployment assets, Community marketplace routes/services/schema, USDT payment workers/routes/settings/schema, and Billing/credits/VIP/membership code paths. README, AGENT, wiki pages, and OpenAPI artifacts now describe the local Gunicorn/nginx, PostgreSQL, Redis, no-paid-product baseline.

Validation evidence is recorded in `task-plans/4phases-checklist.md` and includes compileall, health/OpenAPI/Agent Gateway/backtest tests, OpenAPI export, residual scans, and wiki rebuild/doctor.
