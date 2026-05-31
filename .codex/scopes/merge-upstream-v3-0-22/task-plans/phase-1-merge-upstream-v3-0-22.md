---
description: Task list for upstream remote and v3.0.22 diff discovery.
---

# Tasks: merge-upstream-v3-0-22 Phase 1

## Input

- `AGENT.md`
- `.codex/wiki/reference/source-docs-archive-map.md`
- `.codex/scopes/merge-upstream-v3-0-22/merge-upstream-v3-0-22-implementation-research-notes.md`
- `.codex/scopes/merge-upstream-v3-0-22/task-plans/4phases-checklist.md`

## Canonical Architecture / Key Constraints

- Current branch is `main` tracking `origin/main`.
- No `upstream` remote was configured when this scope was created; the user
  confirmed `https://github.com/brokermr810/QuantDinger`, and it is now added.
- Do not start a merge until the authoritative upstream tag is verified.
- Keep command output free of secrets.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 1: Upstream Discovery And Diff Baseline

Goal: Establish a trusted upstream `v3.0.22` source and pre-merge evidence.

Definition of Done: Upstream URL, tag hash, integration branch, merge base, and
changed-file risk map are recorded in `4phases-checklist.md`.

Tasks:

- [x] T001 [Config] Confirm and add the authoritative upstream remote
  - DoD: `git remote -v` shows the chosen upstream URL and the choice is recorded with evidence; if the expected tag is absent, Phase 1 stops with the exact failed command.
- [x] T002 [QA] Fetch and verify `v3.0.22`
  - DoD: `git ls-remote --tags <upstream> refs/tags/v3.0.22 refs/tags/v3.0.22^{}` and `git fetch <upstream> --tags` succeed, with the tag object/commit recorded.
- [ ] T003 [Config] Create an integration branch from current `main`
  - DoD: A branch such as `merge-upstream-v3.0.22` points at the pre-merge `main` commit and `git status --short --branch` is recorded.
- [x] T004 [Security] Identify high-risk changed paths before merge
  - DoD: `git diff --name-status HEAD...refs/tags/v3.0.22` is reviewed for auth, credential, payment, live trading, migrations, Agent Gateway, env, and CI paths.

Checkpoint: Phase 1 blocks all later phases until the verified tag and risk map
are recorded.

## Dependencies & Execution Order

- Phase 1 blocks all others.
- T001 blocks T002.
- T002 blocks T003 and T004.
- Tasks marked `[P]` may run concurrently only when they do not touch the same files.
