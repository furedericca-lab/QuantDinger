---
title: Source Docs Archive Map
type: reference
status: current
scope: docs-consolidation-2026-05-31
last_checked: 2026-05-31
related_files:
  - README.md
  - AGENT.md
  - .codex/wiki
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
updated: 2026-05-31T16:00:00+08:00
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
- Cloud deployment guides -> `implementation/deployment-and-operations.md`.
- Strategy development, cross-sectional strategy, signal standard, and AI
  trading plan -> `implementation/strategy-backtest-and-execution.md`.
- Agent environment, Agent Gateway, quickstart, MCP setup ->
  `implementation/agent-gateway-and-mcp.md`.
- OAuth, notification, USDT payment guides ->
  `reference/configuration-and-integrations.md`.
- IBKR, MT5, indicators, fast analysis docs -> `reference/broker-and-market-guides.md`.
- Code of conduct, contributing, contributors, security, trademarks, changelog,
  and launch material -> `reference/project-governance.md`.
- Current maintenance/test commands -> `reference/current-verification-commands.md`.

Future durable documentation should be added to `.codex/wiki/` first. README
and AGENT should link to wiki pages or summarize them; they should not grow
into competing manuals.

## Current Documentation Shape

- `README.md` is the operator-facing entry point and should explain access,
  major product workflows, runtime shape, and safety notes.
- `AGENT.md` is the repo-local developer/agent contract and should explain
  source boundaries, high-risk areas, and validation rules.
- `.codex/wiki/index.md` is generated from structured wiki front matter.
- `decision-log.md` and `maintenance-log.md` are generated/maintained wiki
  artifacts.

During upstream merge or rebase, preserve the deletion of the old docs tree
unless the user asks otherwise. If upstream adds new useful docs, extract the
durable facts into the relevant wiki page and update this map.
