---
description: Execution checklist for merging upstream v3.0.22.
---

# Phases Checklist: merge-upstream-v3-0-22

## Input References

- `.codex/scopes/archive/merge-upstream-v3-0-22/merge-upstream-v3-0-22-brainstorming.md`
- `.codex/scopes/archive/merge-upstream-v3-0-22/merge-upstream-v3-0-22-implementation-research-notes.md`
- `.codex/scopes/archive/merge-upstream-v3-0-22/merge-upstream-v3-0-22-scope-milestones.md`
- `.codex/scopes/archive/merge-upstream-v3-0-22/merge-upstream-v3-0-22-technical-documentation.md`
- `.codex/scopes/archive/merge-upstream-v3-0-22/merge-upstream-v3-0-22-contracts.md`
- `AGENT.md`
- `.codex/wiki/reference/source-docs-archive-map.md`

## Global Status Board

| Phase | State | Completion | Health | Blockers |
|---|---|---:|---|---|
| [Phase 1](phase-1-merge-upstream-v3-0-22.md) | Complete | 100% | Healthy | None |
| [Phase 2](phase-2-merge-upstream-v3-0-22.md) | Complete | 100% | Healthy | None |
| [Phase 3](phase-3-merge-upstream-v3-0-22.md) | Complete | 100% | Healthy | None |
| [Phase 4](phase-4-merge-upstream-v3-0-22.md) | Complete | 100% | Healthy | None |

## Phase 1 Execution Record

Completion checklist:

- [x] Authoritative upstream remote URL confirmed.
- [x] `v3.0.22` tag fetched and recorded.
- [x] Integration branch created from current `main`.
- [x] Initial pre-merge diff and high-risk touched areas identified.

Evidence commands:

- Pass: `git remote -v` shows `origin https://github.com/furedericca-lab/QuantDinger` and `upstream https://github.com/brokermr810/QuantDinger`.
- Pass: `git ls-remote --tags upstream refs/tags/v3.0.22 refs/tags/v3.0.22^{}` returned `85024c26dbd140a1ba690df0e553946eb8fe9921 refs/tags/v3.0.22`.
- Pass: `git fetch upstream --tags` fetched `upstream/main` and tags through `v3.0.22`.
- Pass: `git diff --name-status HEAD...refs/tags/v3.0.22` identified high-risk changes in CI, README, version files, Agent Gateway, auth/billing/credential routes, migrations, requirements, OpenAPI, grid services, tests, and `docs/`.
- Pass: branch `merge-upstream-v3.0.22` was created from pre-merge `main` commit `2b5fa5f9990153c149e74dc2d74dde39fe8ad32b`.

Issues/blockers and resolutions:

- Resolved: no `upstream` remote existed at scope creation time; the user confirmed the remote URL and the tag now verifies locally.

Checkpoint confirmation:

- Confirmed.

## Phase 2 Execution Record

Completion checklist:

- [x] Upstream tag merged or replayed on integration branch.
- [x] Conflicts resolved with local security and wiki precedence.
- [x] Version metadata reconciled.
- [x] Changed-file list captured for validation and wiki impact.

Evidence commands:

- Pass with conflicts resolved: `git merge --no-ff refs/tags/v3.0.22`.
- Pass: `git status --short --branch`.
- Pass: `git diff --name-status 2b5fa5f9990153c149e74dc2d74dde39fe8ad32b..HEAD`.

Issues/blockers and resolutions:

- Kept local deletion for `.cursor/skills/quantdinger-agent-workflow/SKILL.md`, `CONTRIBUTING.md`, and old long-form docs.
- Kept narrow OpenAPI artifact exception: `docs/api/*`, `docs/API_CONVENTIONS.md`, and `docs/agent/agent-openapi.json`.
- Preserved local README operator shape and added OpenAPI references.
- Preserved Agent Gateway wiki pointer in `backend_api_python/app/routes/__init__.py`.

Checkpoint confirmation:

- Confirmed. No unresolved merge conflicts remain.

## Phase 3 Execution Record

Completion checklist:

- [x] Version check passes.
- [x] Syntax/import checks pass.
- [x] Targeted tests for changed high-risk modules pass.
- [x] Wiki impact reviewed and wiki rebuilt if needed.
- [x] `git diff --check` passes.

Evidence commands:

- Pass: `python3 scripts/check_version.py` reported canonical `3.0.22`; frontend source paths were skipped because they are not in this checkout.
- Pass: `python3 -m compileall backend_api_python/app mcp_server/src`.
- Pass: `uv run pytest backend_api_python/tests/test_openapi.py backend_api_python/tests/test_agent_v1_saas_guard.py backend_api_python/tests/test_grid_engine.py backend_api_python/tests/test_grid_poller.py backend_api_python/tests/test_strategy_lifecycle.py -q` reported `37 passed`.
- Pass: `cd backend_api_python && SKIP_STARTUP_HOOKS=1 OPENAPI_ENABLED=false uv run python scripts/export_openapi.py --output ../docs/api/openapi.generated.yaml && diff -u ../docs/api/openapi.yaml ../docs/api/openapi.generated.yaml`.
- Pass: `python3 /root/.codex/skills/wiki-note/scripts/wiki.py --root /root/code/QuantDinger rebuild --json`.
- Pass: `python3 /root/.codex/skills/wiki-note/scripts/wiki.py --root /root/code/QuantDinger doctor --json`.
- Pass: `rg -n '^(<<<<<<< |=======$|>>>>>>> )' . --glob '!docs/api/openapi.yaml' --glob '!*.json'`.
- Pass: `git diff --check`.

Issues/blockers and resolutions:

- Fixed one workspace dependency gap by adding OpenAPI dependencies (`flask-smorest`, `marshmallow`, `PyYAML`) to `pyproject.toml` and refreshing `uv.lock`.
- Adjusted `test_grid_poller.py` so the interval test sets last-poll state and the idempotency test mocks the exchange fill query.
- OpenAPI export logs a PostgreSQL connection warning when no `DATABASE_URL` runtime is configured; export still succeeds with `SKIP_STARTUP_HOOKS=1`.

Checkpoint confirmation:

- Confirmed. Phase 3 validation passed.

## Phase 4 Execution Record

Completion checklist:

- [x] Scope evidence updated with final commands and results.
- [x] Final `main` branch is clean before archive move.
- [x] Merge commit created with correct author/committer identity.
- [x] `origin/main` pushed after validation.

Evidence commands:

- Pass before archive: `git status --short --branch` showed `main...origin/main` after pushing merge commit `1141452`.
- Pass: `git log --oneline --decorate -n 5` showed merge commit `1141452`.
- Pass: `git push origin main` pushed `2b5fa5f..1141452`.
- Pending after archive move: archive hygiene scans and archive commit push.

Issues/blockers and resolutions:

- Merge publication complete. Archive move is the remaining closeout change.

Checkpoint confirmation:

- Confirmed for merge publication. Archive publication is recorded by the
  follow-up archive commit.

## Final Release Gate Summary

- Merge implementation was completed and pushed in commit `1141452`.
- Scope was moved to `.codex/scopes/archive/merge-upstream-v3-0-22/` for the
  follow-up archive commit.

## Archive Record

- Archived on 2026-06-01 under `.codex/scopes/archive/merge-upstream-v3-0-22/`.
- Archive purpose: preserve the completed merge-upstream-v3-0-22 audit trail.
- Future enhancements should use a new `repo-task-driven` scope under `.codex/scopes/<enhancement-scope>/`.
- Archived docs should only change for factual errata or path-maintenance updates.
