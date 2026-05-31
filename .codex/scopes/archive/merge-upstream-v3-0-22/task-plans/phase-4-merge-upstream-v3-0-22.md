---
description: Task list for closeout, commit, and push after the v3.0.22 merge.
---

# Tasks: merge-upstream-v3-0-22 Phase 4

## Input

- Completed Phase 3 validation evidence.
- `.codex/scopes/archive/merge-upstream-v3-0-22/task-plans/4phases-checklist.md`
- `AGENT.md`
- `.codex/wiki/maintenance-log.md`

## Canonical Architecture / Key Constraints

- Do not push until validation evidence is recorded.
- Commit author/committer should match the user's GitHub identity when set in
  this repo.
- Keep scope docs accurate; do not mark tasks complete without evidence.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 4: Closeout And Push

Goal: Commit and publish the validated merge with complete audit evidence.

Definition of Done: `main` is clean, `origin/main` contains the merge, and scope
docs record final evidence.

Tasks:

- [ ] T016 [Docs] Finalize scope checklist evidence
  - DoD: `4phases-checklist.md` contains pass/fail results for all executed commands, final status, and residual risk.
- [ ] T017 [QA] Run repo-task scope document checks
  - DoD: `doc_placeholder_scan.sh`, `decision_roundtable_check.sh`, and `scope_sync_check.sh` pass for this scope.
- [ ] T018 [Config] Commit the merge with correct identity
  - DoD: `git config user.name`, `git config user.email`, and `git log -1 --format=fuller` confirm the intended author/committer.
- [ ] T019 [Config] Push to origin
  - DoD: `git push origin main` succeeds and `git status --short --branch` shows `main...origin/main` with no working-tree changes.
- [ ] T020 [Docs] Record post-merge wiki maintenance if needed
  - DoD: `.codex/wiki/maintenance-log.md` records merge-driven wiki updates, or the checklist states why no durable wiki update was needed.

Checkpoint: Scope can be archived only after Phase 4 evidence is complete.

## Dependencies & Execution Order

- Phase 4 depends on Phase 3.
- T016 blocks T017 through T020.
- T018 blocks T019.
- T020 depends on whether Phase 3 changed wiki pages.
