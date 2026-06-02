---
description: Execution checklist for merging upstream v3.0.27.
---

# Phases Checklist: merge-upstream-v3-0-27

## Global Status Board

| Phase | State | Completion | Health | Blockers |
|---|---|---:|---|---|
| Phase 1: Scope and baseline discovery | Complete | 100% | Healthy | None |
| Phase 2: Backend/main repo merge | Complete | 100% | Healthy | None |
| Phase 3: Frontend submodule sync | Complete | 100% | Healthy | None |
| Phase 4: Wiki know-how and validation | Complete | 100% | Healthy | None |

## Phase 1 Execution Record

- [x] Active scope directory created.
- [x] Archived merge and slimdown baselines inspected.
- [x] Upstream remote and tags fetched.
- [x] Initial high-risk diff themes recorded.
- [x] Integration branch created.

Evidence:

- Pass: `repo_task.py inventory --json` reported no active scopes before
  opening this scope.
- Pass: `git fetch upstream --tags --prune` fetched tags through `v3.0.27`.
- Pass: `git rev-parse v3.0.27` resolved target tag.
- Pass: `git -C frontend log --all --grep='v3.0.27'` found frontend release
  commits in the fork history.
- Pass: integration branch `merge-upstream-v3.0.27` was created from current
  `main`.

## Phase 2 Execution Record

- [x] `git merge --no-ff --no-commit v3.0.27` executed.
- [x] Community route/service modify-delete conflicts resolved by preserving
  local deletion.
- [x] Old `docs/STRATEGY_DEV_GUIDE*.md` modify-delete conflicts resolved by
  preserving local docs deletion.
- [x] Indicator route/workspace conflicts resolved by preserving useful
  `asset_type` and script-template filtering while deleting community,
  pricing, VIP-free, review-status, translation, and billing-credit side
  effects.
- [x] Strategy marketplace publish endpoints removed because
  `community_service` remains deleted.
- [x] Upstream scratch files (`_i18n_hits.txt`, `_i18n_state.txt`,
  `_tmp_out.txt`, `backend_api_python/pytest_out.txt`) removed.

Evidence:

- Pass: no unresolved merge conflicts after `git add -u` and adding resolved
  indicator/workspace files.
- Pass: residual scan found no active `community_service`, `billing_service`,
  `usdt_payment`, `publish_to_community`, `pricing_type`, `vip_free`, or
  `review_status` references in active backend route/service code.
- Note: upstream `v3.0.27` keeps repo `VERSION` and backend `_version.py` at
  `3.0.22`; this scope intentionally updates the local main repo version
  constants to `3.0.27` after the merge.

## Phase 3 Execution Record

- [x] Frontend fork release commit found.
- [x] `frontend/` submodule advanced from `92e1da4` to
  `01f3b2ceaa5bf686db9ad5591941bbaf4d260ac3`.
- [x] Frontend dependencies verified with `pnpm install --frozen-lockfile`.
- [x] Frontend production build completed with `pnpm build`.
- [x] `/var/www/quantdinger` replaced with the new `frontend/dist` output.

Evidence:

- Pass: `git -C frontend show 01f3b2c:package.json` confirmed the fork commit
  is reachable; its `package.json` still reports `3.0.22`, matching the
  upstream release-line version constant behavior.
- Pass with warnings: `pnpm build` completed. Warnings are the known Vue2
  `/deep/` CSS minify warnings and large chunk warning.
- Pass: `/var/www/quantdinger/index.html` timestamp updated to
  `2026-06-02 11:32:43 +0800`; deployed file count is `77`.

## Phase 4 Execution Record

- [x] Wiki know-how page created at
  `.codex/wiki/reference/upstream-merge-playbook.md`.
- [x] Source docs archive map now points future release merges to the playbook.
- [x] `AGENTS.md` source-of-truth list now links the playbook.
- [x] Wiki rebuild completed and indexed 11 pages.
- [x] Final validation commands complete.

Validation evidence:

- Pass: `git diff --check`.
- Pass: `python3 scripts/check_version.py` reported canonical `3.0.27`
  after `python3 scripts/bump_version.py 3.0.27`.
- Note: frontend commit `01f3b2c` still carries `package.json` version
  `3.0.22`; that metadata belongs to the frontend submodule repo and should be
  fixed there only if the user wants a frontend fork commit beyond the upstream
  release commit.
- Pass: `python3 -m compileall backend_api_python/app mcp_server/src`.
- Pass: `uv run pytest backend_api_python/tests/test_health.py backend_api_python/tests/test_agent_v1_saas_guard.py backend_api_python/tests/test_indicator_ide_filter.py backend_api_python/tests/test_grid_engine.py backend_api_python/tests/test_grid_poller.py backend_api_python/tests/test_grid_fill_units.py backend_api_python/tests/test_trade_net_pnl.py backend_api_python/tests/test_safe_exec.py -q` reported `62 passed`.
- Pass: OpenAPI export to `.codex/wiki/reference/api/openapi.generated.yaml`
  matched `.codex/wiki/reference/api/openapi.yaml` after updating the artifact
  for new account mirror endpoints.
- Pass: `python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json`
  and `doctor --json`.
- Pass: runtime smoke showed `nginx -t`, active `quantdinger`, `nginx`,
  `cloudflared`, and `postgresql`; loopback `/` and `/api/health` returned
  `200`; public unauthenticated `/api/health` returned Cloudflare Access `302`;
  LAN direct-origin returned `403`.
- Pass: residual scans found only expected baseline warnings, third-party data
  provider "API credits" text, purchased-indicator naming, and frontend
  submodule Docker files. Active billing/community/USDT payment route/service
  imports remain absent.

## Closeout

- Backend/main repo merge resolved on branch `merge-upstream-v3.0.27`.
- Frontend submodule gitlink now points at
  `01f3b2ceaa5bf686db9ad5591941bbaf4d260ac3`.
- Main repo version constants now report `3.0.27`.
- `/var/www/quantdinger` was refreshed from the new `frontend/dist` build.
- Wiki know-how page added at
  `.codex/wiki/reference/upstream-merge-playbook.md`.

## Archive Record

- Archived on 2026-06-02 under `.codex/scopes/archive/merge-upstream-v3-0-27/`.
- Archive purpose: preserve the completed merge-upstream-v3-0-27 audit trail.
- Future enhancements should use a new `repo-task-driven` scope under `.codex/scopes/<enhancement-scope>/`.
- Archived docs should only change for factual errata or path-maintenance updates.
