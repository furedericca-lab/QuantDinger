---
description: Phase 2 tasks for removing the Community marketplace while preserving private indicator workflows.
---

# Tasks: Local Nginx Slimdown Phase 2

## Input

- `backend_api_python/app/routes/community.py`
- `backend_api_python/app/services/community_service.py`
- `backend_api_python/app/openapi/register.py`
- `backend_api_python/migrations/init.sql`
- `backend_api_python/app/routes/indicator.py`
- `.codex/wiki/reference/api/openapi.yaml`
- README, AGENT, and wiki pages that mention Community or marketplace behavior

## Canonical Architecture / Key Constraints

- Community marketplace is removed as an external business feature.
- Core private indicator workspace and strategy code remain in scope.
- Billing dependencies from Community must not be replaced with new payment or
  credit checks.
- OpenAPI artifacts under `.codex/wiki/reference/api/` must stay synchronized.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 2: Community Marketplace Removal

Goal: Remove Community marketplace endpoints, services, schema, docs, and tests
without damaging private indicator and strategy workflows.

Definition of Done: No active Community marketplace API or schema remains, and
private indicator APIs continue to pass focused tests.

Tasks:

- [x] T007 [Backend] Remove Community route and service registration
  - DoD: `backend_api_python/app/routes/community.py` and `backend_api_python/app/services/community_service.py` are removed or emptied from active imports, and `backend_api_python/app/openapi/register.py` no longer registers Community endpoints.
- [x] T008 [Backend] Remove marketplace schema while preserving indicators
  - DoD: `backend_api_python/migrations/init.sql` removes purchase/comment/review marketplace tables and marketplace-only indicator columns while keeping core `qd_indicator_codes` fields required by the private workspace.
- [x] T009 [P] [Docs] Remove Community marketplace documentation
  - DoD: README, AGENT, `.codex/wiki/`, and API docs contain no active Community marketplace product contract.
- [x] T010 [P] [Frontend] Remove or verify absent frontend marketplace calls
  - DoD: Tracked frontend/static source has no calls to removed Community endpoints, or absent frontend source is recorded as a checkpoint risk.
- [x] T011 [QA] Run Phase 2 validation
  - DoD: Run OpenAPI export diff, Spectral lint, relevant backend tests, `git diff --check`, and residual scan for `Community|marketplace|purchase|comment` in active product contexts; record results in the checklist.

Checkpoint: Phase 2 must leave indicator creation, listing, editing, and
strategy use intact before USDT payment removal starts.

## Dependencies & Execution Order

- Phase 2 depends on Phase 1.
- T007 blocks OpenAPI validation.
- T008 must be reviewed with T007 because removed route code may be the only
  consumer of some schema fields.
- T009 and T010 may run in parallel after T007 identifies the final route list.
- T011 runs last and gates Phase 3.
- Parallelization rule: tasks marked `[P]` may run concurrently only if they do not touch the same files.
