---
description: Canonical technical architecture for merging upstream v3.0.22.
---

# merge-upstream-v3-0-22 Technical Documentation

## Canonical Architecture

This repo is a QuantDinger backend-oriented checkout with:

- Flask backend under `backend_api_python/`.
- Canonical first-boot PostgreSQL schema under
  `backend_api_python/migrations/init.sql`.
- MCP wrapper under `mcp_server/`.
- Deployment files at `docker-compose*.yml`, `backend_api_python/Dockerfile`,
  and `backend_api_python/env.example`.
- CI/version checks under `.github/workflows/` and `scripts/`.
- Agent/developer knowledge under `AGENT.md` and `.codex/wiki/`.

The upstream merge should be treated as a source integration task, not a
runtime deployment task.

## Key Constraints And Non-Goals

- Do not weaken JWT, agent-token, credential encryption, safe-exec, or hosted
  trading restrictions.
- Do not store secrets in scope docs or command output.
- Do not restore deleted docs as active sources. Preserve or extract durable
  content into `.codex/wiki/`.
- Do not change external production services during merge validation.
- Do not assume frontend source exists in this checkout.

## Major Decisions and Trade-offs

- Use merge-based integration unless Phase 1 proves another approach is safer.
- Use local repo docs as conflict-resolution policy for documentation layout.
- Use existing scripts for version checking and wiki rebuilds.
- Treat migrations, broker/live-trading code, USDT payment code, auth, and
  Agent Gateway changes as high-risk areas requiring targeted review.

## Module Boundaries And Data Flow

- `backend_api_python/app/routes/` exposes browser, API, and Agent Gateway
  routes.
- `backend_api_python/app/services/` owns domain behavior and broker/trading
  workflows.
- `backend_api_python/app/utils/` owns auth, crypto, database, logging, safe
  execution, and agent helpers.
- `backend_api_python/app/data_sources/` and
  `backend_api_python/app/data_providers/` own market data ingestion and
  normalization.
- `mcp_server/src/quantdinger_mcp/` wraps Agent Gateway REST contracts and must
  not duplicate backend business logic.

## Interfaces And Contracts

Merge resolution must preserve:

- Browser API compatibility for existing routes unless upstream intentionally
  changes them and tests/docs are updated.
- Agent Gateway `/api/agent/v1` scope, audit, idempotency, and hosted-mode
  boundaries.
- Environment variable semantics documented in `backend_api_python/env.example`.
- Docker Compose service names and frontend-backend network assumptions unless
  upstream explicitly requires a coordinated change.

## Operational Behavior

The scope does not deploy services. Runtime checks may be added in later phases
only if the merge touches Compose, entrypoints, migrations, background workers,
or config loading.

## Observability And Error Handling

Conflict resolution should preserve existing logging and fail-closed behavior in
security-sensitive paths. Do not replace explicit denial paths with silent
fallbacks.

## Security Model And Hardening Notes

Review these paths carefully when touched by upstream:

- `backend_api_python/app/utils/auth.py`
- `backend_api_python/app/routes/auth.py`
- `backend_api_python/app/utils/agent_auth.py`
- `backend_api_python/app/utils/credential_crypto.py`
- `backend_api_python/app/utils/safe_exec.py`
- `backend_api_python/app/services/usdt_payment*`
- `backend_api_python/app/services/live_trading/`
- `backend_api_python/migrations/init.sql`

## Test Strategy Mapping

- Version: `python scripts/check_version.py`
- Syntax: `python3 -m compileall backend_api_python/app mcp_server/src`
- Tests: targeted `pytest` suites matching touched files, then broader backend
  tests if risk warrants.
- Docs/wiki: `wiki.py rebuild --json`, `wiki.py doctor --json`, and
  repo-task scope scans.
- Git hygiene: `git diff --check`, `git status --short --branch`.
