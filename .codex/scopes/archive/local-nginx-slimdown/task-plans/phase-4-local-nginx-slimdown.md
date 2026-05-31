---
description: Phase 4 tasks for deep removal of Billing, credits, and VIP.
---

# Tasks: Local Nginx Slimdown Phase 4

## Input

- `backend_api_python/app/routes/billing.py`
- `backend_api_python/app/services/billing_service.py`
- `backend_api_python/app/routes/auth.py`
- `backend_api_python/app/services/oauth_service.py`
- `backend_api_python/app/routes/fast_analysis.py`
- `backend_api_python/app/routes/strategy.py`
- `backend_api_python/app/routes/portfolio_monitor.py`
- `backend_api_python/app/routes/user.py`
- `backend_api_python/app/routes/indicator.py`
- `backend_api_python/app/routes/settings.py`
- `backend_api_python/env.example`
- `backend_api_python/migrations/init.sql`
- `.codex/wiki/reference/api/openapi.yaml`
- README, AGENT, and wiki pages that mention Billing, credits, VIP, or membership

## Canonical Architecture / Key Constraints

- Billing, credits, VIP, and membership are removed deeply, not disabled.
- AI, indicator, strategy, fast analysis, and portfolio monitor workflows should
  execute without credit checks or refunds.
- OAuth, Turnstile, email, SMS, Telegram, brokers, Agent Gateway, and MCP remain.
- External paid functionality is not required by the operator.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 4: Billing, Credits, And VIP Deep Removal

Goal: Remove Billing, credits, VIP, membership fields, and all call sites from
the backend, schema, docs, API contract, and settings surfaces.

Definition of Done: No active paid feature or credit/VIP gate remains, and core
AI/analysis/strategy flows run without billing checks.

Tasks:

- [x] T018 [Backend] Remove Billing route and service modules
  - DoD: `backend_api_python/app/routes/billing.py` and `backend_api_python/app/services/billing_service.py` are removed from active imports, route registration, OpenAPI registration, and tests.
- [x] T019 [Backend] Remove credits and VIP schema fields
  - DoD: `backend_api_python/migrations/init.sql` removes user credits/VIP columns, credit log tables, membership order tables, and billing settings rows.
- [x] T020 [Backend] Remove registration and OAuth credit grants
  - DoD: `backend_api_python/app/routes/auth.py` and `backend_api_python/app/services/oauth_service.py` no longer grant registration credits, VIP, referral credits, or membership state.
- [x] T021 [Backend] Remove AI and analysis billing gates
  - DoD: `backend_api_python/app/routes/fast_analysis.py`, `backend_api_python/app/routes/strategy.py`, `backend_api_python/app/routes/indicator.py`, and `backend_api_python/app/routes/portfolio_monitor.py` no longer call `check_and_consume`, refund credits, return `insufficient_credits`, or branch on VIP state.
- [x] T022 [Backend] Remove user/admin credit endpoints
  - DoD: `backend_api_python/app/routes/user.py` no longer exposes credit adjustment, credit log, membership, or USDT rescue/order administration.
- [x] T023 [Config] Remove billing settings and env examples
  - DoD: `backend_api_python/app/routes/settings.py` and `backend_api_python/env.example` no longer expose Billing, credits, VIP, membership, or payment configuration.
- [x] T024 [P] [Frontend] Remove or verify absent client calls to Billing/credits/VIP APIs
  - DoD: Tracked frontend/static source has no calls or labels for removed Billing, credits, VIP, membership, or payment endpoints, or absent frontend source is recorded as a checkpoint risk.
- [x] T025 [Docs] Remove paid feature documentation and update wiki
  - DoD: README, AGENT, and `.codex/wiki/` describe the local non-paid product baseline and contain no active Billing/credits/VIP/membership contract.
- [x] T026 [QA] Run Phase 4 validation and residual scans
  - DoD: Run OpenAPI export diff, Spectral lint, backend health/agent/backtest tests, import checks, wiki rebuild/doctor, `git diff --check`, and residual scans for `Billing|billing|credits|VIP|membership|insufficient_credits|check_and_consume|refund`.

Checkpoint: Phase 4 completes the active scope when validation passes and the
checklist contains final evidence for all phases.

## Dependencies & Execution Order

- Phase 4 depends on Phases 1-3.
- T018 and T019 define the deletion boundary and should run before call-site
  cleanup.
- T020 through T023 may be batched by touched module after T018 identifies
  import failures.
- T024 can run in parallel with docs if it does not touch the same files.
- T026 runs last and is the release/archive gate.
- Parallelization rule: tasks marked `[P]` may run concurrently only if they do not touch the same files.
