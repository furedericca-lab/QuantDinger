---
description: Phase 3 tasks for removing USDT payment and membership purchase behavior.
---

# Tasks: Local Nginx Slimdown Phase 3

## Input

- `backend_api_python/app/routes/billing.py`
- `backend_api_python/app/services/usdt_payment_service.py`
- `backend_api_python/app/services/usdt_payment/`
- `backend_api_python/app/__init__.py`
- `backend_api_python/app/routes/settings.py`
- `backend_api_python/env.example`
- `backend_api_python/migrations/init.sql`
- README, AGENT, and wiki pages that mention USDT payment or membership purchase

## Canonical Architecture / Key Constraints

- Remove payment/membership USDT behavior only.
- Preserve trading, market-data, broker, quick-trade, and strategy symbols that
  contain `USDT`.
- Preserve OAuth, Turnstile, email, SMS, Telegram, Agent Gateway, and MCP.
- Phase 4 will remove the broader Billing/credits/VIP service and fields.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 3: USDT Payment And Membership Purchase Removal

Goal: Delete payment-specific USDT services, watchers, env/settings, schema, and
API behavior while preserving crypto trading symbols.

Definition of Done: No USDT payment or membership purchase runtime code remains,
and legitimate trading `USDT` references are reviewed and retained.

Tasks:

- [x] T012 [Backend] Remove USDT payment service modules and startup hooks
  - DoD: `backend_api_python/app/services/usdt_payment_service.py`, `backend_api_python/app/services/usdt_payment/`, and `start_usdt_order_worker` startup hooks are removed from active imports and startup.
- [x] T013 [Backend] Remove payment route subpaths and membership purchase behavior
  - DoD: Billing route subpaths for `/api/billing/usdt/*` and membership purchase/order behavior are removed without introducing replacement payment code.
- [x] T014 [Config] Remove USDT payment env and settings
  - DoD: `backend_api_python/env.example` and `backend_api_python/app/routes/settings.py` no longer expose USDT payment, payment watcher, membership purchase, receiving-address, or chain watcher settings.
- [x] T015 [Backend] Remove USDT payment schema
  - DoD: `backend_api_python/migrations/init.sql` removes USDT payment order tables and payment-specific membership order links that are no longer consumed.
- [x] T016 [P] [Docs] Remove USDT payment documentation
  - DoD: README, AGENT, and `.codex/wiki/` no longer describe USDT payment or membership purchase operation.
- [x] T017 [QA] Run Phase 3 validation and USDT residual review
  - DoD: Run route/OpenAPI tests, startup/import checks, `git diff --check`, and `rg -n "USDT|usdt_payment|USDT_PAY|membership|payment" backend_api_python README.md AGENT.md .codex/wiki`; record which `USDT` hits are preserved trading symbols.

Checkpoint: Phase 3 must leave no payment worker or payment setting before
Phase 4 removes the rest of Billing, credits, and VIP.

## Dependencies & Execution Order

- Phase 3 depends on Phases 1-2.
- T012 should run before T013 so route imports cannot trigger removed workers.
- T014 and T015 should run after T013 identifies final payment settings/schema.
- T016 may run in parallel after T013.
- T017 runs last and gates Phase 4.
- Parallelization rule: tasks marked `[P]` may run concurrently only if they do not touch the same files.
