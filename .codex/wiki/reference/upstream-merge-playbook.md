---
title: Upstream Merge Playbook
type: reference
status: current
scope: quantdinger-upstream-merge
last_checked: 2026-06-02
related_files:
  - path: .codex/scopes/archive/merge-upstream-v3-0-22
    role: prior-merge
  - path: .codex/scopes/archive/local-nginx-slimdown
    role: baseline
  - path: .codex/scopes/merge-upstream-v3-0-27
    role: active-scope
  - path: AGENTS.md
    role: contract
  - path: README.md
    role: operator-entrypoint
  - path: frontend
    role: submodule
code_anchors:
  - id: upstream-merge-scope-archive
    kind: scope-archive
    file: .codex/scopes/archive/merge-upstream-v3-0-22/merge-upstream-v3-0-22-scope-milestones.md
    symbol: merge-upstream-v3-0-22 Scope And Milestones
    role: precedent
  - id: local-nginx-slimdown-baseline
    kind: scope-archive
    file: .codex/scopes/archive/local-nginx-slimdown/local-nginx-slimdown-contracts.md
    symbol: Contracts: Local Nginx Slimdown
    role: baseline
tags:
  - upstream
  - merge
  - baseline
  - submodule
updated: 2026-06-02T12:02:00+08:00
---

# Upstream Merge Playbook

Use this page as the standard operating procedure for merging a new upstream
QuantDinger release tag. It captures the reusable judgement from the
`v3.0.22` and `v3.0.27` merge work so future merges can move quickly without
weakening the local baseline.

## Standard Flow

1. Preflight:
   - confirm the working tree is clean;
   - fetch `origin`, `upstream`, and frontend submodule refs;
   - verify the target upstream tag and candidate frontend commit;
   - inspect archived scopes for local baseline constraints.
2. Open scope:
   - create `.codex/scopes/merge-upstream-v<target>/`;
   - record target refs, baseline constraints, high-risk diff themes, and
     intended validation commands before resolving conflicts.
3. Merge backend/main repo:
   - merge with `git merge --no-ff --no-commit v<target>`;
   - classify conflicts as Accept, Adapt, Reject, or Escalate;
   - preserve local wiki/no-paid-product/local-nginx/frontend-submodule
     baseline.
4. Sync frontend:
   - advance only the `frontend/` submodule gitlink;
   - build the submodule;
   - deploy `frontend/dist` to `/var/www/quantdinger` only after the build
     succeeds.
5. Migrate artifacts and docs:
   - update repo `VERSION` and backend `APP_VERSION` to the target semver;
   - regenerate OpenAPI into `.codex/wiki/reference/api/openapi.yaml`;
   - update README/AGENTS/wiki when operator or agent behavior changes;
   - record merge know-how, if any new conflict pattern appears.
6. Validate:
   - run syntax, targeted tests, OpenAPI diff, wiki doctor, residual scans,
     frontend build, and runtime smoke.
7. Close:
   - update scope evidence;
   - commit the merge;
   - push only when the user asks or the scope explicitly requires it.

## Baseline To Defend

The active local baseline is not upstream's default product shape:

- Runtime is local Gunicorn plus nginx, PostgreSQL, Redis, Cloudflare Tunnel,
  and Cloudflare Access on `https://tsw.momoe.qzz.io`.
- Documentation is wiki-first. API artifacts live under `.codex/wiki/`, not
  active `docs/api` or `docs/agent` paths.
- Frontend source is the `frontend/` submodule pointing at
  `https://github.com/furedericca-lab/QuantDinger-Vue`.
- Docker Compose, Dockerfiles, GHCR publishing, Railway config, and
  container-first deployment are retired from the active local baseline.
- Billing, credits, VIP, membership purchase, Community marketplace, and USDT
  payment are retired product surfaces.

When a conflict touches these areas, default to the local baseline unless the
user explicitly changes it.

## Fast Triage

Run these before opening a merge:

```bash
git status --short --ignore-submodules=none
git fetch upstream --tags --prune
git rev-parse v<target>
git diff --name-status HEAD..v<target> | sed -n '1,240p'
git -C frontend fetch origin --tags --prune
git -C frontend log --oneline --decorate --all --grep='v<target>'
```

Classify the diff into four buckets:

- Accept: backend fixes, tests, market data, grid/live trading improvements,
  safe-exec hardening, Agent Gateway fixes, and broker correctness changes that
  do not depend on retired surfaces.
- Adapt: changes that add useful behavior but refer to deleted docs,
  marketplace fields, or Docker paths. Keep the useful behavior and rewrite the
  references to local wiki/runtime paths.
- Reject: active `docs/` tree restoration, Docker/Railway/GHCR deployment
  files, billing/community/USDT payment modules, purchase schema, or credit/VIP
  gates.
- Escalate: auth, credential encryption, live order submission, migrations, or
  Agent Gateway trading-scope behavior where the safe resolution is not clear.

## Migration Checklist

Run this checklist after conflicts are resolved and before commit:

- Version:
  - `VERSION` equals the target release semver, for example `3.0.27`.
  - `backend_api_python/app/_version.py` has the same `APP_VERSION`.
  - `python3 scripts/check_version.py` passes.
  - Frontend package metadata is checked separately in the frontend submodule;
    do not let stale frontend package metadata block the main repo version
    unless the user wants a frontend fork commit.
- API artifacts:
  - `backend_api_python/scripts/export_openapi.py` writes to
    `.codex/wiki/reference/api/openapi.yaml`.
  - Generated OpenAPI and committed OpenAPI match after accepting API changes.
  - Old `docs/api` and `docs/agent` artifact paths remain absent.
- Removed product surfaces:
  - No active imports of `community_service`, `billing_service`, or
    `usdt_payment`.
  - No active routes under Community, Billing, USDT payment, purchase,
    marketplace publish, credits, VIP, or membership.
  - No schema columns/tables for credits/VIP/payment/community are added back.
  - Do not remove crypto symbols containing `USDT`.
- Deployment baseline:
  - Docker Compose, backend Dockerfile, Railway config, GHCR publishing, and
    container-first docs remain absent from active local paths.
  - nginx/Gunicorn/PostgreSQL/Redis/Cloudflare Tunnel guidance remains the
    operator baseline.
- Frontend:
  - `git submodule status` shows the intended frontend commit.
  - `pnpm install --frozen-lockfile` and `pnpm build` pass in `frontend/`.
  - `/var/www/quantdinger` is refreshed from `frontend/dist` when deploying
    the merge locally.
- Scope evidence:
  - `.codex/scopes/merge-upstream-v<target>/task-plans/4phases-checklist.md`
    records conflict decisions and command results.
  - New recurring conflict patterns are added to this playbook.

## Conflict Resolution Rules

- Preserve `.codex/wiki/`, `.codex/scopes/archive/`, `AGENTS.md`, README local
  operator shape, `.gitmodules`, and `frontend/`.
- Keep `docs/api/openapi.yaml`, `docs/api/index.html`,
  `docs/agent/agent-openapi.json`, and `docs/API_CONVENTIONS.md` out of active
  paths. Their local homes are `.codex/wiki/reference/api/`,
  `.codex/wiki/reference/agent/`, and
  `.codex/wiki/reference/api-conventions.md`.
- If upstream adds useful docs, summarize durable facts into the relevant wiki
  page and update `reference/source-docs-archive-map.md`.
- If upstream adds community, billing, credits, VIP, membership, purchase, or
  USDT payment code, delete the product surface and then scan for imports and
  schema residue.
- Do not remove market symbols containing `USDT`; trading pairs are different
  from USDT payment workflow code.
- For frontend, advance only the submodule gitlink. Do not vendor frontend
  source into the backend repo.

## Version Policy

The repo-root `VERSION` is the local main-repo release line. After merging
upstream release tag `vX.Y.Z`, set `VERSION` and backend `APP_VERSION` to
`X.Y.Z` unless the user explicitly wants to preserve a lower upstream constant.

Use:

```bash
python3 scripts/bump_version.py X.Y.Z
python3 scripts/check_version.py
```

Frontend version metadata is owned by the frontend submodule repo. If the
frontend release commit still says an older version in `package.json`, record
it in scope evidence. Only create a frontend fork commit to fix that metadata
when the user wants the submodule's own version display corrected.

## Known v3.0.27 Patterns

The `v3.0.27` merge showed these concrete patterns:

- `backend_api_python/app/routes/indicator.py` gained useful `asset_type`
  handling for script templates, but also restored community publish,
  `pricing_type`, `vip_free`, review status, translation, and billing credit
  checks. Keep `asset_type`; remove the commercial side effects.
- `backend_api_python/app/services/indicator_workspace.py` gained useful
  script-template filtering, but its authoring contract pointed back to old
  docs and its insert SQL included marketplace fields. Keep filtering; point
  docs to the wiki and keep private indicator inserts.
- `backend_api_python/app/routes/strategy.py` restored marketplace publish
  endpoints that import `community_service`. Remove those endpoints if
  `community_service` stays deleted.
- The frontend fork may not expose release tags even when release commits are
  present. Use `git -C frontend log --all --grep='v<target>'`, record the exact
  commit, and build the submodule to verify.

## Residual Scans

After resolving conflicts, run targeted scans:

```bash
rg -n "community_service|routes/community|billing_service|routes/billing|usdt_payment|USDT payment|publish_to_community|pricing_type|vip_free|review_status|credits|VIP|membership|marketplace|purchase" backend_api_python README.md AGENTS.md .codex/wiki .github scripts mcp_server -S
find docs -maxdepth 3 -type f 2>/dev/null | sort
find . -maxdepth 2 \( -name 'docker-compose*.yml' -o -name 'Dockerfile' -o -name 'railway.json' -o -name '.dockerignore' \) -print | sort
rg -n "^(<<<<<<< |=======$|>>>>>>> )" . --glob '!frontend/**' --glob '!*.json'
```

Review hits instead of deleting blindly. Expected benign hits include baseline
warnings in README/AGENTS/wiki, third-party data-provider "API credits" text,
crypto trading pairs such as `BTC/USDT`, and Docker files inside the frontend
submodule.

## Validation Profile

Minimum closeout checks for release merges:

```bash
git diff --check
python3 scripts/check_version.py
python3 -m compileall backend_api_python/app mcp_server/src
uv run pytest backend_api_python/tests/test_health.py backend_api_python/tests/test_agent_v1_saas_guard.py backend_api_python/tests/test_indicator_ide_filter.py -q
cd frontend && pnpm install --frozen-lockfile && pnpm build
python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json
python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json
```

Broaden tests when the merge touches broker execution, grid fills, migrations,
safe execution, Agent Gateway scopes, or authentication.

## Closeout Evidence Template

Record the following in the active scope before committing:

```text
- Backend target: upstream vX.Y.Z at <hash>
- Frontend target: furedericca-lab/QuantDinger-Vue at <hash>
- Version constants: VERSION=<X.Y.Z>, APP_VERSION=<X.Y.Z>
- Conflict decisions: accept/adapt/reject/escalate summary
- OpenAPI: regenerated and diff clean
- Frontend: pnpm install/build result and deployed dist timestamp
- Runtime: service state, loopback API/WebUI, public Access redirect, LAN 403
- Residual scans: hits reviewed and classified
- Tests: exact commands and pass/fail counts
```
