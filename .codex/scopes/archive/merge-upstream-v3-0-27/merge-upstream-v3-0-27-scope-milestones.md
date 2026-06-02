---
description: Scope boundaries and milestones for merging upstream v3.0.27.
---

# merge-upstream-v3-0-27 Scope And Milestones

## In Scope

- Open an active repo-task scope for the `v3.0.27` merge.
- Merge upstream backend/main-repo changes through `v3.0.27`.
- Preserve the local nginx/no-paid-product/wiki-first/submodule baseline.
- Advance the frontend submodule to the matching `v3.0.27` source commit.
- Build or otherwise validate the frontend source state.
- Write merge know-how into `.codex/wiki/` for future release merges.
- Commit the validated result.

## Out Of Scope

- Changing Cloudflare hostname, Access policy, secrets, database credentials,
  or production account settings.
- Restoring Docker/Railway/GHCR/container-first deployment as the active local
  baseline.
- Restoring billing, credits, VIP, community marketplace, membership purchase,
  or USDT payment functionality.
- Reintroducing the old `docs/` tree as active documentation.
- Deleting archived scope history.

## Milestones

1. Scope and baseline discovery:
   - Scope docs exist and record archive-derived constraints.
   - Upstream and frontend target commits are verified.
2. Backend/main repo merge:
   - Upstream `v3.0.27` is merged on an integration branch.
   - Conflicts are resolved with local baseline precedence.
3. Frontend submodule sync:
   - `frontend/` points at the matching fork `v3.0.27` commit.
   - Frontend install/build or equivalent source validation is recorded.
4. Wiki know-how and validation:
   - Reusable merge triage know-how is written to `.codex/wiki/`.
   - Focused tests, wiki checks, and residual scans are recorded.
5. Closeout:
   - Scope evidence is updated.
   - Final commit is created, and push is performed if requested or needed for
     continuity.

## Decision Log

| Decision | Evidence | Result |
|---|---|---|
| Use phased scope | Merge spans backend, docs, frontend submodule, and wiki. | Four-phase evidence plus closeout |
| Preserve local docs model | `AGENTS.md`, archived `merge-upstream-v3-0-22`, and source docs archive map. | Keep `.codex/wiki/`, do not restore active legacy docs |
| Preserve no-paid-product baseline | Archived `local-nginx-slimdown` scope. | Reject billing/community/USDT payment restoration |
| Advance frontend through submodule | Current README/AGENTS and `.gitmodules`. | Update `frontend/` gitlink, not vendored source |

## Exit Criteria

- No unresolved merge conflicts.
- `frontend/` points at the selected `v3.0.27` frontend commit.
- README/AGENTS/wiki describe the resulting baseline accurately.
- Residual scans do not reveal restored active retired surfaces.
- Validation commands are recorded with pass/fail details.
