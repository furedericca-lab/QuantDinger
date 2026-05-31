---
description: Scope boundaries and milestones for merging upstream v3.0.22.
---

# merge-upstream-v3-0-22 Scope and Milestones

## In Scope

- Use the confirmed upstream remote
  `https://github.com/brokermr810/QuantDinger` for `v3.0.22`.
- Fetch upstream tags and compare the current branch with `v3.0.22`.
- Merge upstream release changes into the current QuantDinger backend checkout.
- Resolve conflicts in backend, config, CI, docs, wiki, and MCP files.
- Update version metadata using existing scripts and checks.
- Run focused validation for changed modules and broad syntax/version checks.
- Update `.codex/wiki/` if the merge changes durable product, operation,
  security, or architecture knowledge.
- Commit and push the completed merge after evidence is recorded.

## Out Of Scope

- Rewriting already-pushed local history without explicit user approval.
- Restoring the deleted legacy `docs/` tree as an active documentation source.
- Migrating frontend source into this repo.
- Rotating secrets, changing production credentials, or editing `.env` values.
- Deploying production services unless separately requested.

## Decision Log

| Boundary / Decision | Evidence Source | Evidence Strength | Conflict | Confidence | Confidence Reason | Result |
|---|---|---:|---|---:|---|---|
| Active scope is phased | User request; repo-task-driven skill | 5 | none | 5 | Merge scope is cross-cutting and needs evidence. | Use four phases |
| Upstream remote setup is a gate | `git remote -v`; `git ls-remote --tags upstream refs/tags/v3.0.22` | 5 | resolved | 5 | User confirmed the remote URL and the tag now resolves. | Phase 1 remote/tag tasks complete |
| Preserve wiki docs model | `AGENT.md`; source docs archive wiki page | 5 | none | 5 | Local guidance explicitly rejects restoring deleted legacy docs during normal maintenance. | Resolve docs conflicts into wiki |
| Push only after validation | User pattern and repo-task workflow | 4 | none | 4 | User usually wants commit/push after completed validation, but this scope is only creation until implementation starts. | Record as final phase gate |

## Milestones

1. Upstream discovery and diff baseline:
   - Authoritative upstream URL and `v3.0.22` tag are verified.
   - Pre-merge branch, base commit, and diff summary are recorded.
2. Merge and conflict resolution:
   - Upstream release changes are merged on an integration branch.
   - Conflicts are resolved with documented local policy precedence.
3. Validation and wiki alignment:
   - Version checks, syntax/import checks, targeted tests, and wiki checks pass
     or failures are recorded with fixes.
4. Closeout and push:
   - Scope evidence is complete.
   - Final merge commit is on `main` and pushed to `origin/main`.

## Dependencies

- Milestone 2 depends on Milestone 1.
- Milestone 3 depends on Milestone 2.
- Milestone 4 depends on Milestone 3.
- Wiki alignment depends on the final changed-file set from Milestone 2.

## Exit Criteria

- `git status --short --branch` is clean on `main` after closeout.
- `origin/main` contains the validated merge.
- Version metadata and release tag expectations are consistent.
- `.codex/wiki/` and active scope evidence reflect any durable knowledge
  changes from upstream.
- No secrets or private credentials appear in diffs, logs, or scope docs.

## Escalation Triggers

- The verified upstream repository does not contain `v3.0.22`.
- Upstream changes conflict with local auth, credential encryption, hosted-mode
  trading restrictions, or Agent Gateway security semantics.
- Merge resolution would require deleting user/local commits or rewriting
  pushed history.
- Upstream introduces migrations that cannot be safely ordered from local
  evidence.
- The user asks for a deployment, tag publication, or external-account action
  beyond normal git push.
