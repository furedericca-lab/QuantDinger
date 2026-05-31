---
description: Implementation research notes for merging upstream v3.0.22.
---

# merge-upstream-v3-0-22 Implementation Research Notes

## Problem Statement And Current Baseline

The user requested an active scope for merging upstream `v3.0.22` into
`/root/code/QuantDinger`.

Current evidence from 2026-06-01:

- `git status --short --branch` reported `## main...origin/main` before scope
  creation.
- `git remote -v` showed only
  `origin https://github.com/furedericca-lab/QuantDinger`.
- `git ls-remote --tags upstream refs/tags/v3.0.22` failed because `upstream`
  is not configured.
- User-confirmed correction: upstream is
  `https://github.com/brokermr810/QuantDinger`.
- Updated Phase 1 evidence: `git remote add upstream
  https://github.com/brokermr810/QuantDinger` succeeded;
  `git ls-remote --tags upstream refs/tags/v3.0.22 refs/tags/v3.0.22^{}` returned
  `85024c26dbd140a1ba690df0e553946eb8fe9921 refs/tags/v3.0.22`; `git fetch
  upstream --tags` fetched `upstream/main` and tags through `v3.0.22`.
- Recent history contains local commits after an upstream-looking `v3.0.21`
  commit: `2b5fa5f Improve wiki navigation metadata`, `5543cfc Use uv commands
  in docs`, `5c10168 Add uv workspace environment`, `9e33062 Consolidate docs
  into wiki`, then `9a35ade v3.0.21`.
- `backend_api_python/app/_version.py` currently contains `APP_VERSION =
  "3.0.20"`, so version metadata must be checked during the merge.

## Gap Analysis With Evidence

- Upstream remote/tag gap: resolved for the URL and tag. Remaining Phase 1 work
  is creating the integration branch and recording the full pre-merge risk map.
- Documentation model gap: `.codex/wiki/reference/source-docs-archive-map.md`
  says the old `docs/` tree was consolidated into `.codex/wiki/` and should not
  be restored during upstream merges unless explicitly requested.
- Release metadata gap: `.github/workflows/basic-ci.yml` runs
  `python scripts/check_version.py`; version updates must use the existing
  scripts rather than ad hoc string edits.
- Validation gap: the repo has backend Python tests, `pyproject.toml`, uv
  workspace files, Docker/Compose files, MCP server files, and wiki tooling.
  The merge plan needs staged validation instead of a single final smoke test.

## Architecture / Implementation Options And Trade-offs

| Option | Trade-off | Fit |
|---|---|---|
| Configure `upstream`, fetch `v3.0.22`, merge the tag into `main` | Safest history preservation; conflict resolution may be broad | Preferred default |
| Create a temporary integration branch before merging | Adds one branch but keeps `main` stable until verified | Recommended if conflicts are non-trivial |
| Cherry-pick upstream range | Smaller batches but weaker provenance and higher chance of missed commits | Use only if tag merge is unsuitable |
| Rebase local commits on upstream tag | Clean history but rewrites pushed commits | Out of scope unless the user explicitly asks |

## Decision Roundtable

| Decision | Requirement Clarity | Evidence Strength | Evidence Source | Conflict | User-Intent Confidence | Implementation Confidence | Risk/Reversibility | Confidence Reason | Outcome |
|---|---:|---:|---|---|---:|---:|---:|---|---|
| Create a phased active scope | 5 | 5 | User request plus repo-task-driven workflow | none | 5 | 5 | 3 | Merge to upstream release is multi-file and evidence-heavy. | Accepted |
| Gate work on upstream remote/tag verification | 5 | 5 | `git remote -v`; successful `git ls-remote --tags upstream refs/tags/v3.0.22` | resolved | 5 | 5 | 3 | Remote is now configured and the tag resolves to commit `85024c26dbd140a1ba690df0e553946eb8fe9921`. | Accepted |
| Prefer merge commit over rebase | 4 | 4 | pushed `origin/main` history; local commits after v3.0.21 | none | 4 | 4 | 3 | Preserves pushed local changes and avoids history rewrite. | Accepted |
| Preserve wiki consolidation during conflicts | 5 | 5 | `AGENT.md`; `.codex/wiki/reference/source-docs-archive-map.md` | none | 5 | 4 | 3 | Local docs model is explicit and recently updated. | Accepted |

## Selected Design And Rationale

Use a temporary integration branch from current `main`, configure/fetch the
verified upstream repository, merge `refs/tags/v3.0.22`, resolve conflicts with
local policy precedence, validate, then fast-follow docs/wiki and push to
`origin/main` after user-approved closeout.

Local precedence during conflict resolution:

1. Preserve secrets, auth, credential encryption, Agent Gateway scope checks,
   and hosted-mode trading restrictions.
2. Preserve `.codex/wiki/` as the durable knowledge layer and avoid restoring
   deleted long-form docs as active sources.
3. Accept upstream bug fixes and release changes unless they conflict with
   local security, deployment, or agent-facing architecture.
4. Keep `README.md` operator-facing and `AGENT.md` agent/developer-facing.

## Test And Validation Strategy

Minimum commands to record before closeout:

- `git status --short --branch`
- `git remote -v`
- `git ls-remote --tags <upstream> refs/tags/v3.0.22 refs/tags/v3.0.22^{}`
- `git diff --name-status <pre-merge>..HEAD`
- `python scripts/check_version.py`
- `python3 -m compileall backend_api_python/app mcp_server/src`
- targeted `pytest` for changed backend tests
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py --root /root/code/QuantDinger rebuild --json`
- `python3 /root/.codex/skills/wiki-note/scripts/wiki.py --root /root/code/QuantDinger doctor --json`
- `git diff --check`

Broader checks are required if the merge touches Docker, migrations, auth,
credentials, live trading, payments, Agent Gateway, or MCP.

## Risks, Assumptions, Unresolved Questions

- Confirmed: upstream is the public GitHub repository
  `https://github.com/brokermr810/QuantDinger`, and `v3.0.22` is available.
- Risk: upstream may change database migrations or first-boot schema in ways
  that require migration ordering review.
- Risk: upstream may reintroduce deleted docs; useful durable content should be
  moved into `.codex/wiki/` instead.
- Risk: frontend-related upstream changes may not apply cleanly because this
  checkout treats frontend source as external/private.
