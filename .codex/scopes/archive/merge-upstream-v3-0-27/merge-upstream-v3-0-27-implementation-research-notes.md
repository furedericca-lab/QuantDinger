---
description: Research notes for merging upstream v3.0.27 while preserving the local QuantDinger baseline.
---

# merge-upstream-v3-0-27 Implementation Research Notes

## Baseline Evidence

- Current branch: `main`.
- Current origin: `https://github.com/furedericca-lab/QuantDinger`.
- Current upstream: `https://github.com/brokermr810/QuantDinger`.
- Current backend public runtime baseline: local Gunicorn behind nginx and
  Cloudflare Tunnel on `https://tsw.momoe.qzz.io`.
- Current frontend source baseline: `frontend/` submodule at
  `92e1da4c68d353505a3c1c04ad5a9a9f383d0540` (`v3.0.22`).

Archived scope inputs:

- `.codex/scopes/archive/merge-upstream-v3-0-22/`: prior upstream merge
  workflow and conflict-resolution evidence.
- `.codex/scopes/archive/local-nginx-slimdown/`: local nginx/no-paid-product
  baseline and removed surface inventory.

## Initial Remote Evidence

- `git fetch upstream --tags --prune` fetched upstream tags through
  `v3.0.27`.
- `git rev-parse v3.0.27` resolved to
  `e5e9b96b381d66687a98a82e5381d523218b23c8`.
- The `v3.0.27` tag object subject displayed as upstream release metadata;
  merge should use the tag ref and record final merge parent.
- Upstream `v3.0.27` still contains `VERSION=3.0.22` and
  `APP_VERSION = "3.0.22"`, but the local main repo release line should report
  the target tag after the merge. This scope updates local `VERSION` and
  backend `APP_VERSION` to `3.0.27`.
- Frontend fork history contains a matching `v3.0.27` commit:
  `01f3b2c` and a signed release commit `59ff6eb`.

## High-Risk Diff Themes

Initial `git diff --name-status HEAD..v3.0.27` shows upstream would restore or
move many files that conflict with the local baseline:

- Deletes local `.codex/wiki/` and archived scope docs from upstream's view.
- Deletes local `.gitmodules` and `AGENTS.md` from upstream's view.
- Adds Docker, Compose, Railway, GHCR, top-level governance docs, and old
  `docs/` content.
- Adds Community, Billing, USDT payment, and related schemas/tests.
- Touches auth, Agent Gateway, safe exec, migrations, live trading, grid, data
  providers, OpenAPI, and tests.

## Merge Strategy

1. Use an integration branch from current `main`.
2. Merge upstream `v3.0.27` without rewriting history.
3. Preserve local deletions for retired docs/deploy/monetization surfaces.
4. Accept upstream backend improvements only when they do not depend on retired
   surfaces.
5. Update frontend submodule to the matching fork commit after backend merge
   conflicts are resolved.
6. Write a wiki know-how page summarizing the reusable merge triage method.

## Validation Profile

Minimum expected checks:

- `git diff --check`
- `python3 scripts/check_version.py`
- `python3 -m compileall backend_api_python/app mcp_server/src`
- Focused pytest selection for changed high-risk backend modules.
- OpenAPI export to `.codex/wiki/reference/api/openapi.yaml` or generated diff.
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json`
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json`
- Residual scans for active `docs/api`, `docs/agent`, billing/community/USDT
  payment, Docker/GHCR/Railway restoration.
