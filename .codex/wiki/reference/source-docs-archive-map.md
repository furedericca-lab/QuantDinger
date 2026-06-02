---
title: Source Docs Archive Map
type: reference
status: current
scope: docs-consolidation-2026-05-31
last_checked: 2026-06-01
related_files:
  - path: README.md
    role: doc
  - path: AGENTS.md
    role: doc
  - path: .codex/wiki
    role: doc
  - path: .codex/wiki/index.md
    role: generated
  - path: .codex/wiki/maintenance-log.md
    role: doc
  - path: .codex/wiki/reference/api/openapi.yaml
    role: generated
  - path: .codex/wiki/reference/api/index.html
    role: generated
  - path: .codex/wiki/reference/agent/agent-openapi.json
    role: generated
code_anchors:
  - id: docs-consolidation-wiki-index
    kind: generated-doc
    file: .codex/wiki/index.md
    symbol: Project Wiki Index
    role: references
  - id: docs-consolidation-maintenance-log
    kind: log
    file: .codex/wiki/maintenance-log.md
    symbol: Maintenance Log
    role: references
source_docs:
  - docs
  - CODE_OF_CONDUCT.md
  - CONTRIBUTING.md
  - CONTRIBUTORS.md
  - DEVELOPMENT.md
  - SECURITY.md
  - TRADEMARKS.md
tags:
  - docs
  - archive-map
updated: 2026-06-01T00:42:00+08:00
---

# Source Docs Archive Map

The previous `docs/` markdown set and top-level governance files were
consolidated into `.codex/wiki/` on 2026-05-31. The intent is to keep one
agent-readable knowledge layer and a concise README entrypoint.

## Mapping

- Multilingual README files -> `concepts/product-architecture.md` and the new
  `README.md`.
- Backend README and development guide -> `concepts/product-architecture.md`,
  `implementation/deployment-and-operations.md`, and `project-governance.md`.
- Cloud deployment guides -> archived historical context; current deployment is
  local Gunicorn/nginx in `implementation/deployment-and-operations.md`.
- Strategy development, cross-sectional strategy, signal standard, and AI
  trading plan -> `implementation/strategy-backtest-and-execution.md`.
- Agent environment, Agent Gateway, quickstart, MCP setup ->
  `implementation/agent-gateway-and-mcp.md`.
- OAuth and notification guides ->
  `reference/configuration-and-integrations.md`.
- IBKR, MT5, indicators, fast analysis docs -> `reference/broker-and-market-guides.md`.
- Code of conduct, contributing, contributors, security, trademarks, changelog,
  and launch material -> `reference/project-governance.md`.
- Current maintenance/test commands -> `reference/current-verification-commands.md`.
- API conventions, OpenAPI export rules, and the API artifact locations ->
  `reference/api-conventions.md`.

Future durable documentation should be added to `.codex/wiki/` first. README
and AGENTS should link to wiki pages or summarize them; they should not grow
into competing manuals.

## Current Documentation Shape

- `README.md` is the operator-facing entry point and should explain access,
  major product workflows, runtime shape, and safety notes.
- `AGENTS.md` is the repo-local developer/agent contract and should explain
  source boundaries, high-risk areas, and validation rules.
- `.codex/wiki/index.md` is generated from structured wiki front matter.
- `decision-log.md` and `maintenance-log.md` are generated/maintained wiki
  artifacts.

During upstream merge or rebase, preserve the deletion of the old docs tree
unless the user asks otherwise. If upstream adds new useful docs, extract the
durable facts into the relevant wiki page and update this map.

## API Artifacts

The API documentation and generated artifacts now live under `.codex/wiki/`:

- `.codex/wiki/reference/api-conventions.md`
- `.codex/wiki/reference/api/openapi.yaml`
- `.codex/wiki/reference/api/index.html`
- `.codex/wiki/reference/agent/agent-openapi.json`

These files support OpenAPI export, lint, browsing, and client integration
without keeping a separate `docs/` documentation tree.
