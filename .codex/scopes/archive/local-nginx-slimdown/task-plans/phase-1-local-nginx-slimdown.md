---
description: Phase 1 tasks for replacing container/cloud deployment guidance with a local nginx baseline.
---

# Tasks: Local Nginx Slimdown Phase 1

## Input

- `README.md`
- `AGENT.md`
- `.codex/wiki/implementation/deployment-and-operations.md`
- `.codex/wiki/reference/current-verification-commands.md`
- `.codex/wiki/reference/configuration-and-integrations.md`
- `docker-compose.yml`, `docker-compose.build.yml`, `docker-compose.ghcr.yml`
- `backend_api_python/Dockerfile`, `backend_api_python/docker-entrypoint.sh`
- `.github/workflows/docker-publish.yml`
- `backend_api_python/railway.json`, `mcp_server/railway.json`

## Canonical Architecture / Key Constraints

- Target runtime is local backend/Gunicorn plus nginx reverse proxy.
- Preserve Agent Gateway, `mcp_server/`, broker integrations, OAuth,
  Turnstile, email, SMS, and Telegram.
- Do not delete tests, OpenAPI CI, `backend_api_python/run.py`,
  `backend_api_python/gunicorn_config.py`, `backend_api_python/env.example`,
  `backend_api_python/migrations/init.sql`, `pyproject.toml`, or lockfiles.
- Do not restore the legacy `docs/` tree.

## Format

- `[ID] [P?] [Component] Description`
- `[P]` means parallelizable.
- Valid `Component` values: `Backend`, `Frontend`, `Agentic`, `Docs`, `Config`, `QA`, `Security`, `Infra`.
- Every task must include a clear DoD.

## Phase 1: Local Nginx Deployment Baseline

Goal: Remove container/cloud deployment assumptions and make local nginx the
documented runtime baseline.

Definition of Done: The active repo no longer presents Docker/Railway/GHCR as
the current deployment path, while preserved integrations and tests remain
available.

Tasks:

- [x] T001 [Infra] Remove container/cloud distribution assets
  - DoD: Remove or retire `docker-compose.yml`, `docker-compose.build.yml`, `docker-compose.ghcr.yml`, `backend_api_python/Dockerfile`, `backend_api_python/docker-entrypoint.sh`, `.dockerignore`, `backend_api_python/.dockerignore`, `mcp_server/.dockerignore`, `.github/workflows/docker-publish.yml`, `backend_api_python/railway.json`, and `mcp_server/railway.json` after confirming no preserved runtime path imports them.
- [x] T002 [Config] Remove Docker-specific CI/install assumptions
  - DoD: Remove Docker publish and compose-check jobs from active CI/install surfaces while keeping OpenAPI and backend test validation paths.
- [x] T003 [Docs] Rewrite deployment docs for backend/Gunicorn plus nginx
  - DoD: Update `README.md`, `AGENT.md`, `.codex/wiki/implementation/deployment-and-operations.md`, and `.codex/wiki/reference/current-verification-commands.md` with local service startup, nginx reverse proxy, PostgreSQL, Redis, and health checks.
- [x] T004 [P] [Agentic] Verify MCP and Agent Gateway preservation
  - DoD: `mcp_server/`, `backend_api_python/app/routes/agent_v1/`, Agent OpenAPI docs, and MCP README remain present and no deployment cleanup removes their build/test paths.
- [x] T005 [P] [Security] Verify preserved secret and auth boundaries
  - DoD: `backend_api_python/env.example` still documents OAuth, Turnstile, email, SMS, Telegram, broker, LLM, JWT, and database secrets without Docker-only wording.
- [x] T006 [QA] Run Phase 1 validation
  - DoD: Run `git diff --check`, OpenAPI health tests, wiki rebuild/doctor, and record results in `task-plans/4phases-checklist.md`.

Checkpoint: Phase 1 blocks all others. The active operator path must be local
nginx before feature removals begin.

## Dependencies & Execution Order

- T001 and T002 should run before T003 so docs describe the actual file state.
- T004 and T005 may run in parallel after T001.
- T006 runs last and gates Phase 2.
- Parallelization rule: tasks marked `[P]` may run concurrently only if they do not touch the same files.
