---
description: Task list for merging upstream v3.0.22 and resolving conflicts.
---

# Tasks: merge-upstream-v3-0-22 Phase 2

## Input

- Phase 1 verified upstream tag and changed-file map.
- `.codex/scopes/merge-upstream-v3-0-22/merge-upstream-v3-0-22-scope-milestones.md`
- `.codex/scopes/merge-upstream-v3-0-22/merge-upstream-v3-0-22-technical-documentation.md`
- `AGENT.md`
- `.codex/wiki/index.md`

## Canonical Architecture / Key Constraints

- Preserve local security and docs policy during conflicts.
- Do not reintroduce active legacy docs; route durable content into wiki.
- Do not rewrite pushed history.
- Treat migrations, auth, credentials, payments, broker execution, Agent
  Gateway, and config as high-risk conflict areas.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 2: Merge And Conflict Resolution

Goal: Integrate upstream `v3.0.22` into the local branch while preserving local
policy and product boundaries.

Definition of Done: The merge is conflict-free, version metadata is reconciled,
and the changed-file list is ready for validation.

Tasks:

- [ ] T005 [Config] Merge the verified upstream tag on the integration branch
  - DoD: `git merge --no-ff refs/tags/v3.0.22` either completes or leaves conflicts that are listed in `4phases-checklist.md`.
- [ ] T006 [Security] Resolve security-sensitive conflicts deliberately
  - DoD: Conflicts in auth, credential crypto, safe execution, Agent Gateway, payments, live trading, and migrations are resolved with explicit notes in the checklist.
- [ ] T007 [Docs] Preserve wiki-first documentation structure
  - DoD: Useful upstream docs are represented in `.codex/wiki/` or README/AGENT entry points as appropriate, and deleted legacy docs are not restored as active docs unless the user explicitly directs it.
- [ ] T008 [Config] Reconcile version and release metadata
  - DoD: `VERSION`, `backend_api_python/app/_version.py`, workflow tag assumptions, and any upstream version changes are consistent or the mismatch is recorded for Phase 3 fixes.
- [ ] T009 [QA] Capture the post-merge changed-file set
  - DoD: `git diff --name-status <pre-merge>..HEAD` is recorded and used to select Phase 3 tests.

Checkpoint: Phase 2 must leave no unresolved merge conflicts before Phase 3.

## Dependencies & Execution Order

- Phase 2 depends on Phase 1.
- T005 blocks T006 through T009.
- T006 and T007 may run in parallel only when they touch disjoint files.
- Phase 3 depends on a conflict-free working tree.
