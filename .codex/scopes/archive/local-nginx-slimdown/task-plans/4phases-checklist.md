---
description: Execution checklist for the four-phase local nginx slimdown.
---

# Phases Checklist: Local Nginx Slimdown

## Input References

- `.codex/scopes/archive/local-nginx-slimdown/local-nginx-slimdown-implementation-research-notes.md`
- `.codex/scopes/archive/local-nginx-slimdown/local-nginx-slimdown-scope-milestones.md`
- `.codex/scopes/archive/local-nginx-slimdown/local-nginx-slimdown-technical-documentation.md`
- `.codex/scopes/archive/local-nginx-slimdown/local-nginx-slimdown-contracts.md`
- `.codex/scopes/archive/local-nginx-slimdown/task-plans/phase-1-local-nginx-slimdown.md`
- `.codex/scopes/archive/local-nginx-slimdown/task-plans/phase-2-local-nginx-slimdown.md`
- `.codex/scopes/archive/local-nginx-slimdown/task-plans/phase-3-local-nginx-slimdown.md`
- `.codex/scopes/archive/local-nginx-slimdown/task-plans/phase-4-local-nginx-slimdown.md`

## Global Status Board

| Phase | State | Completion | Health | Blockers |
| --- | --- | --- | --- | --- |
| Phase 1: Local nginx deployment baseline | Complete | 100% | Validated | None |
| Phase 2: Community marketplace removal | Complete | 100% | Validated | None |
| Phase 3: USDT payment and membership purchase removal | Complete | 100% | Validated | None |
| Phase 4: Billing, credits, and VIP deep removal | Complete | 100% | Validated | None |

## Phase Entries

- [Phase 1](phase-1-local-nginx-slimdown.md)
- [Phase 2](phase-2-local-nginx-slimdown.md)
- [Phase 3](phase-3-local-nginx-slimdown.md)
- [Phase 4](phase-4-local-nginx-slimdown.md)

## Phase 1 Execution Record

Completion checklist:

- [x] Container/cloud deployment files removed or retired.
- [x] README, AGENT, and wiki updated to local nginx baseline.
- [x] OpenAPI, MCP, broker, OAuth, Turnstile, and notification surfaces checked.

Evidence commands:

- `git ls-files | rg '(^docker-compose|Dockerfile|docker|railway|billing|community|usdt_payment|test_usdt_payment|test_market_indicator_score)'` identified the tracked removal set.
- `uv run python -m compileall -q backend_api_python/app backend_api_python/scripts` passed.
- `uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py -q` passed: 26 tests.

Issues/blockers and resolutions:

- Root `.env.example`, compose files, Dockerfiles, Railway configs, and Docker publish workflow were removed; CI now validates backend syntax/import/version instead of compose config.

Checkpoint confirmation:

- Confirmed. Operator docs now describe local PostgreSQL/Redis, Gunicorn or `python run.py`, and nginx reverse proxy.

## Phase 2 Execution Record

Completion checklist:

- [x] Community marketplace routes/services unregistered and removed.
- [x] Marketplace schema/docs/OpenAPI/tests removed or updated.
- [x] Core indicator workspace behavior preserved.

Evidence commands:

- `rg -n "billing_service|get_billing_service|usdt_payment|qd_usdt_orders|qd_membership_orders|qd_credits_log|set-credits|credits-log|set-vip|vip_expires_at|vip_|membership|Billing|billing|Community|community|marketplace|publish_to_community|pricing_type|vip_free|review_status|qd_indicator_purchases|qd_indicator_comments|insufficient_credits|check_and_consume|USDT_PAY|USDT payment" backend_api_python/app backend_api_python/tests backend_api_python/migrations/init.sql backend_api_python/env.example backend_api_python/requirements.txt -g '*.py' -g '*.sql' -g '*.example' -g 'requirements.txt' -S` returned no matches.
- `cd backend_api_python && SKIP_STARTUP_HOOKS=1 OPENAPI_ENABLED=false ../.venv/bin/python scripts/export_openapi.py --output ../.codex/wiki/reference/api/openapi.generated.yaml` passed.
- `rg -n "Billing|billing|Community|community|marketplace|set-credits|credits-log|set-vip|vip_|membership|USDT payment|usdt|/api/billing|/api/community" .codex/wiki/reference/api/openapi.generated.yaml -S` returned no matches.

Issues/blockers and resolutions:

- Private indicator save/list paths were simplified to user-owned indicators only; marketplace-only columns and tables were removed from first-boot schema.

Checkpoint confirmation:

- Confirmed. OpenAPI no longer exposes Community endpoints.

## Phase 3 Execution Record

Completion checklist:

- [x] USDT payment services, watchers, startup hooks, env/settings, schema, and tests removed.
- [x] Trading and market-data `USDT` symbol usage reviewed and preserved.
- [x] OpenAPI and wiki no longer describe payment USDT behavior.

Evidence commands:

- `uv run python -m compileall -q backend_api_python/app backend_api_python/scripts` passed.
- `uv run python -m pytest backend_api_python/tests/test_openapi.py -q` passed: 5 tests.
- Residual code scan above returned no payment `USDT` matches in backend code, tests, schema, env example, or requirements; market/trading symbol references are outside payment workflow and preserved.

Issues/blockers and resolutions:

- `start_usdt_order_worker`, `app.services.usdt_payment*`, billing route subpaths, USDT env/settings, and USDT order schema were removed.

Checkpoint confirmation:

- Confirmed. No payment worker or payment setting remains.

## Phase 4 Execution Record

Completion checklist:

- [x] Billing routes/services/imports removed.
- [x] Credits/VIP fields, tables, API responses, settings, and admin endpoints removed.
- [x] Registration, OAuth, AI, fast analysis, strategy, portfolio monitor, and indicator call sites no longer consume/refund/check credits.
- [x] Residual scans contain no active Billing/credits/VIP product contract in backend implementation surfaces.

Evidence commands:

- `uv run python -m pytest backend_api_python/tests/test_health.py -q` passed: 1 test.
- `uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py -q` passed: 26 tests.
- `uv run python -m pytest backend_api_python/tests/test_backtest_execution.py backend_api_python/tests/test_trading_execution_modes.py -q` passed: 9 tests.
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json` passed.
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json` passed.

Issues/blockers and resolutions:

- User/admin credit and VIP routes plus USDT order rescue endpoints were removed from `user.py`; user list/export/profile no longer select or attach billing fields.

Checkpoint confirmation:

- Confirmed. Scope implementation is complete and ready for final archive checks.

## Final Release Gate Summary

Required before archive or push:

- `git diff --check`
- `bash /root/.codex/skills/repo-task-driven/scripts/doc_placeholder_scan.sh .codex/scopes/archive/local-nginx-slimdown`
- `bash /root/.codex/skills/repo-task-driven/scripts/decision_roundtable_check.sh .codex/scopes/archive/local-nginx-slimdown`
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json`
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json`
- `.venv/bin/python -m pytest backend_api_python/tests/test_openapi.py -q`
- `.venv/bin/python -m pytest backend_api_python/tests/test_health.py backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py -q`
- `.venv/bin/python -m pytest backend_api_python/tests/test_backtest_execution.py -q`
- OpenAPI export diff and Spectral lint after route removals.

## Archive Record

- Archived on 2026-06-01. Archived scope path:
  `.codex/scopes/archive/local-nginx-slimdown/`.
