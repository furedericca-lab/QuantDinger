---
title: Project Governance
type: reference
status: current
scope: quantdinger-governance
last_checked: 2026-05-31
related_files:
  - LICENSE
  - README.md
  - AGENT.md
source_docs:
  - CODE_OF_CONDUCT.md
  - CONTRIBUTING.md
  - CONTRIBUTORS.md
  - DEVELOPMENT.md
  - SECURITY.md
  - TRADEMARKS.md
  - docs/CHANGELOG.md
  - docs/LAUNCH_MATERIALS.md
tags:
  - governance
  - security
  - trademarks
  - contributing
updated: 2026-05-31T15:50:00+08:00
---

# Project Governance

## Scope

This page consolidates repository governance, contribution, security, release,
and branding guidance.

## Contribution Model

Useful contributions include core backend engineering, strategy and research
work, documentation and examples, security hardening, and product explanation.

Pull requests should be focused, explain behavioral impact, include relevant
tests, and avoid mixing unrelated refactors with feature changes.

Recommended PR contents:

- problem statement and user-facing impact;
- changed files grouped by product area;
- migration/config impact;
- risk notes for auth, credentials, billing, agent scopes, or live trading;
- tests or smoke checks run;
- screenshots only when UI behavior changed.

Do not mix formatting-only refactors with behavior changes in high-risk areas.

## Security Policy

Security-sensitive areas include auth, JWT, OAuth, agent tokens, credential
encryption, the safe execution sandbox, live trading order paths, multi-user
tenant isolation, billing, and USDT payment flows.

Reports should include impact, reproduction steps, affected version or commit,
and whether credentials or funds may be exposed. Do not publish exploit details
before maintainers have time to respond.

High-risk paths:

- `backend_api_python/app/utils/auth.py`
- `backend_api_python/app/utils/agent_auth.py`
- `backend_api_python/app/routes/agent_v1/`
- `backend_api_python/app/utils/credential_crypto.py`
- `backend_api_python/app/utils/safe_exec.py`
- `backend_api_python/app/services/live_trading/`
- `backend_api_python/app/services/pending_order_worker.py`
- `backend_api_python/app/services/trading_executor.py`
- `backend_api_python/app/services/usdt_payment/`
- `backend_api_python/app/routes/billing.py`
- `backend_api_python/migrations/init.sql`
- `mcp_server/src/quantdinger_mcp/server.py`

When touching these paths, validate denial paths, redaction, tenant isolation,
and runtime configuration impact.

## Code Of Conduct

Project participation requires respectful, constructive behavior. Harassment,
threats, privacy violations, spam, and bad-faith disruption are not acceptable.
Maintainers may moderate issues, pull requests, discussions, and community
channels to protect project health.

## Trademarks And Branding

The Apache 2.0 license covers code. It does not grant unrestricted rights to
the QuantDinger name, marks, logos, or branding.

Forks and commercial redistributions should use distinct branding unless
permission is granted. Do not imply official endorsement, partnership, or
ownership of the QuantDinger project.

Runtime branding can be configured through environment/settings values such as
app name, logo URLs, legal URLs/text, contact links, and social links. Runtime
rebranding does not change trademark ownership.

## Release Notes

Future release notes should record version, date, user-visible features,
security changes, database migrations, upgrade notes, key files, and tests.

## Documentation Ownership

The old long-form `docs/` tree and top-level governance markdown files were
consolidated into `.codex/wiki/`.

Rules:

- README is the operator-facing entry point.
- `AGENT.md` is the developer/agent operating contract.
- `.codex/wiki/` is the durable manual.
- `.codex/scopes/<scope>/` is for active task contracts when used.
- `.codex/scopes/archive/<scope>/` is for completed task provenance when used.
- Do not create new `docs/<topic>.md` files unless the user explicitly asks or
  a product distribution requirement demands tracked docs outside the wiki.

## Verification

For documentation-only changes:

```bash
python3 /root/.codex/skills/wiki-note/scripts/wiki_note.py rebuild --json
python3 /root/.codex/skills/wiki-note/scripts/wiki_note.py lint --json
```

For code changes, pair docs updates with the focused test family listed in
[Current Verification Commands](current-verification-commands.md).
