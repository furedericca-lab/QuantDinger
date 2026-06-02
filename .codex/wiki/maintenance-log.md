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

## 2026-06-02T11:37:00Z [merge-upstream-v3-0-27]

- Summary: Recorded the reusable upstream release-merge playbook while merging backend changes through v3.0.27 and advancing the frontend submodule to the matching fork commit.
- Pages: .codex/wiki/reference/upstream-merge-playbook.md, .codex/wiki/reference/source-docs-archive-map.md, .codex/wiki/reference/api/openapi.yaml
- Verification: frontend pnpm build, targeted pytest, OpenAPI export diff, wiki rebuild/doctor, nginx/runtime smoke, Cloudflare Access and LAN direct-origin checks.
- Residual risk: The frontend release commit still reports package metadata 3.0.22; main repo VERSION and backend APP_VERSION were updated to 3.0.27, and frontend metadata should be fixed only through a frontend fork commit if needed.

## 2026-06-02T12:10:00Z [frontend-v3-0-28-submodule]

- Summary: Advanced the frontend submodule to furedericca-lab/QuantDinger-Vue commit 0c659aa, whose package and UI metadata report 3.0.28, while keeping the backend/main repo at 3.0.27.
- Pages: README.md, AGENTS.md, .codex/wiki/maintenance-log.md
- Verification: frontend pnpm build, wiki rebuild/doctor, local nginx static asset smoke, backend /api/health smoke.
- Residual risk: The version pairing is intentionally frontend 3.0.28 plus backend 3.0.27; future backend merges should revisit the pairing before bumping main repo VERSION.
