---
description: Task list for validating the upstream v3.0.22 merge.
---

# Tasks: merge-upstream-v3-0-22 Phase 3

## Input

- Phase 2 changed-file set.
- `scripts/check_version.py`
- Backend test suite under `backend_api_python/tests/`.
- `.codex/wiki/` and wiki-note CLI.

## Canonical Architecture / Key Constraints

- Validation must map to changed files; high-risk changes require targeted
  tests or manual smoke evidence.
- Wiki must be rebuilt if durable project knowledge changes.
- If validation fails, fix the merge and rerun the failed check before closeout.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 3: Validation And Knowledge Alignment

Goal: Prove the merged tree is internally consistent and that durable knowledge
is current.

Definition of Done: Version, syntax, targeted tests, wiki checks, and git
hygiene checks pass or have fixed/re-run evidence.

Tasks:

- [ ] T010 [QA] Run version validation
  - DoD: `python scripts/check_version.py` passes or version files are fixed and the command is rerun successfully.
- [ ] T011 [QA] Run Python syntax/import compilation
  - DoD: `python3 -m compileall backend_api_python/app mcp_server/src` passes.
- [ ] T012 [QA] Run changed-module tests
  - DoD: Targeted `pytest` commands are selected from the Phase 2 changed-file set and pass; if broad backend tests are required, the command and result are recorded.
- [ ] T013 [Security] Validate high-risk denial paths when touched
  - DoD: Auth, agent-token, credential, safe-exec, payment, and live-trading changes have targeted test or review evidence.
- [ ] T014 [Docs] Align wiki and scope evidence
  - DoD: `wiki.py rebuild --json`, `wiki.py doctor --json`, and any needed wiki page updates are completed; if no wiki update is needed, the reason is recorded.
- [ ] T015 [QA] Run final git hygiene checks
  - DoD: `git diff --check` and `git status --short --branch` are recorded.

Checkpoint: Phase 3 blocks commit/push until all required validation has pass
evidence or an explicitly recorded residual risk accepted by the user.

## Dependencies & Execution Order

- Phase 3 depends on Phase 2.
- T010 and T011 may run before targeted tests.
- T012 and T013 depend on the changed-file map.
- T014 depends on the final documentation/wiki diff.
- Phase 4 depends on Phase 3.
