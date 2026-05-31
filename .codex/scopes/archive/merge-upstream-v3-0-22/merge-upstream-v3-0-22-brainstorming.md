---
description: Brainstorming and decision framing for merging upstream v3.0.22.
---

# merge-upstream-v3-0-22 Brainstorming

## Problem

Bring QuantDinger forward to the upstream `v3.0.22` release without losing the
local repo's agent knowledge layer, CI/workspace changes, or security posture.
At scope creation the checkout had only `origin` configured and no `upstream`
remote. The user confirmed the upstream as
`https://github.com/brokermr810/QuantDinger`, and Phase 1 evidence now verifies
that remote and the `v3.0.22` tag.

## Scope

- Use `upstream=https://github.com/brokermr810/QuantDinger` as the verified
  source remote for `v3.0.22`.
- Fetch and inspect `refs/tags/v3.0.22`.
- Merge or replay upstream changes onto the current `main` branch.
- Preserve local `.codex/wiki/`, `.codex/scopes/`, `AGENT.md`, README entry
  point semantics, uv workspace files, and Agent Gateway/security additions.
- Update version metadata, tests, wiki notes, and release evidence after the
  merge.

## Constraints

- Do not reintroduce the deleted legacy `docs/` tree as active documentation.
  Extract useful upstream doc changes into `.codex/wiki/`.
- Do not discard local commits with reset/rebase cleanup unless the user
  explicitly authorizes that operation.
- Do not expose `.env`, tokens, broker keys, OAuth secrets, cookies, or private
  credentials in logs or scope evidence.
- Keep frontend source boundaries intact. This repo uses a backend checkout and
  prebuilt/private frontend model, not a tracked frontend source tree.

## Options

| Option | Use Case | Pros | Cons |
|---|---|---|---|
| Merge `upstream/v3.0.22` into `main` | Default path after tag verification | Preserves local history and makes conflict resolution auditable | Can produce merge conflicts across docs, version files, and backend services |
| Cherry-pick upstream commits from local base to `v3.0.22` | Upstream tag is linear but merge would import unwanted history | Allows smaller conflict batches | Requires careful range selection and can miss merge commits |
| Rebase local commits onto `v3.0.22` | Only if user asks for rewritten history | Produces linear history | Rewrites already-pushed commits and is higher risk |

## Decision Summary

| Decision | Options Considered | Rationale | Research Note Link |
|---|---|---|---|
| Use a phased scope | Single-contract vs phased | A release merge can touch backend, config, docs, CI, and wiki; phased evidence is safer. | `merge-upstream-v3-0-22-implementation-research-notes.md` |
| Prefer merge commit after tag verification | Merge, cherry-pick, rebase | Current branch has pushed local commits on `origin/main`; a merge preserves history and avoids silent loss. | `merge-upstream-v3-0-22-implementation-research-notes.md` |
| Treat upstream remote discovery as Phase 1 gate | Assume remote vs verify remote | Creation-time evidence showed only `origin`; user then confirmed `https://github.com/brokermr810/QuantDinger`, and `git ls-remote --tags upstream refs/tags/v3.0.22` succeeded. | `merge-upstream-v3-0-22-implementation-research-notes.md` |

## Decision

Proceed with a four-phase merge scope:

1. Verify upstream remote/tag and establish the exact diff boundary.
2. Merge and resolve conflicts while preserving local architecture and docs.
3. Run focused and broad validation, including wiki impact.
4. Record final evidence, commit, and push only after validation passes.

## Risks

- Upstream may not expose `v3.0.22` from the expected source repository.
- Upstream docs may conflict with the local wiki consolidation.
- Version constants may already drift: `backend_api_python/app/_version.py`
  reports `3.0.20` while recent local history includes a `v3.0.21` commit.
- Upstream may alter auth, billing, broker credential handling, or live trading
  paths; these areas require security-focused review.

## Open Questions

- None for the upstream URL. It is now confirmed as
  `https://github.com/brokermr810/QuantDinger`.
