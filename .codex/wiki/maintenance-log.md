---
title: Maintenance Log
type: maintenance-log
status: current
updated: 2026-05-31T12:34:09Z
---

# Maintenance Log

Append-only history for wiki updates caused by scope work, implementation closeout, or knowledge refresh.

## 2026-05-31T16:42:00Z [merge-upstream-v3-0-22]

- Summary: Recorded upstream v3.0.22 merge knowledge for OpenAPI artifacts, Agent Gateway self-service token management, and grid runtime fill polling.
- Pages: .codex/wiki/implementation/agent-gateway-and-mcp.md, .codex/wiki/implementation/strategy-backtest-and-execution.md, .codex/wiki/reference/source-docs-archive-map.md, .codex/wiki/reference/current-verification-commands.md
- Verification: uv run pytest targeted merge suite, OpenAPI export diff, wiki.py rebuild/doctor pending in scope closeout.
- Residual risk: Database-backed runtime behavior was not smoke-tested because no DATABASE_URL/PostgreSQL runtime is configured in this checkout.

## 2026-05-31T16:14:59Z [quantdinger-wiki-navigation]

- Summary: Upgraded QuantDinger wiki to role-aware related_files, code_anchors, generated navigation indexes, and removed obsolete .codex/notepad.md scratch surface.
- Pages: .codex/wiki/index.md, .codex/wiki/.index/code-map.json
- Verification: python3 /root/.codex/skills/wiki-note/scripts/wiki.py --root /root/code/QuantDinger doctor --json, python3 /root/.codex/skills/wiki-note/scripts/wiki.py --root /root/code/QuantDinger nav search 'agent token scope hosted paper only quick trade' --json
- Residual risk: Navigation anchors are curated from current source names; future code renames should update related_files and code_anchors.

## 2026-05-31T18:02:59Z [local-nginx-slimdown]

- Summary: Synchronized local nginx/no-paid-product baseline after removing Docker, billing, USDT payment, community marketplace, credits, VIP, and membership surfaces.
- Pages: .codex/wiki/implementation/deployment-and-operations.md, .codex/wiki/reference/configuration-and-integrations.md, .codex/wiki/reference/current-verification-commands.md, .codex/wiki/concepts/product-architecture.md
- Verification: OpenAPI export, targeted pytest, wiki rebuild/doctor
