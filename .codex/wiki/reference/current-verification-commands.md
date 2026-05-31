---
title: Current Verification Commands
type: reference
status: current
scope: quantdinger-verification
last_checked: 2026-06-01
related_files:
  - path: README.md
    role: doc
  - path: AGENT.md
    role: doc
  - path: docker-compose.yml
    role: config
  - path: backend_api_python
    role: owner
  - path: docs/api/openapi.yaml
    role: generated
  - path: docs/agent/agent-openapi.json
    role: generated
  - path: mcp_server
    role: owner
  - path: .codex/wiki
    role: doc
code_anchors:
  - id: verification-agent-gateway-tests
    kind: command
    file: backend_api_python/tests/test_agent_v1.py
    symbol: test_agent_v1
    role: tests
  - id: verification-strategy-runtime-tests
    kind: command
    file: backend_api_python/tests/test_backtest_execution.py
    symbol: test_backtest_execution
    role: tests
  - id: verification-wiki-maintenance
    kind: command
    file: .codex/wiki
    symbol: wiki.py doctor
    role: references
  - id: verification-openapi-export
    kind: command
    file: backend_api_python/scripts/export_openapi.py
    symbol: export_openapi
    role: tests
source_docs:
  - README.md
  - AGENT.md
tags:
  - verification
  - tests
  - operations
updated: 2026-06-01T00:42:00+08:00
---

# Current Verification Commands

## Scope

Use this page as the quick command map for QuantDinger maintenance. Prefer the
narrowest meaningful check first, then broaden to Compose/runtime checks when
the change affects deployment behavior.

## General Backend

```bash
uv run python -m pytest backend_api_python/tests/test_health.py
uv run python -m py_compile <changed-file.py>
```

## Agent Gateway

```bash
uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py
uv run python -m pytest backend_api_python/tests/test_openapi.py
uv run python -m py_compile backend_api_python/app/routes/agent_v1/__init__.py
uv run python -m py_compile backend_api_python/app/utils/agent_auth.py
uv run python -m py_compile backend_api_python/app/utils/agent_jobs.py
```

## OpenAPI

```bash
cd backend_api_python
SKIP_STARTUP_HOOKS=1 OPENAPI_ENABLED=false uv run python scripts/export_openapi.py --output ../docs/api/openapi.generated.yaml
diff -u ../docs/api/openapi.yaml ../docs/api/openapi.generated.yaml
rm -f ../docs/api/openapi.generated.yaml
```

## Strategy, Backtest, And Trading Semantics

```bash
uv run python -m pytest backend_api_python/tests/test_backtest_execution.py backend_api_python/tests/test_trading_execution_modes.py
uv run python -m pytest backend_api_python/tests/test_grid_engine.py backend_api_python/tests/test_grid_poller.py
uv run python -m py_compile backend_api_python/app/services/backtest.py
uv run python -m py_compile backend_api_python/app/services/trading_executor.py
uv run python -m py_compile backend_api_python/app/services/pending_order_worker.py
```

Use signal or paper mode for live-order-adjacent checks unless the user
explicitly authorizes a real account action.

## Billing And USDT Payments

```bash
uv run python -m pytest backend_api_python/tests/test_usdt_payment_idempotency.py
uv run python -m py_compile backend_api_python/app/routes/billing.py
uv run python -m py_compile backend_api_python/app/services/usdt_payment/service.py
```

## MCP Server

```bash
uv run python -m py_compile mcp_server/src/quantdinger_mcp/server.py
uv run --directory mcp_server python -m build
```

`uv run --directory mcp_server python -m build` requires the locked local build
dependencies to be installed. If they are missing, run `uv sync` first.

## Compose Runtime

```bash
docker compose config
docker compose ps
docker compose logs --tail=100 backend
curl -f http://localhost:5000/api/health
```

Use these after deployment, env, image, port, database, Redis, worker, or
reverse-proxy changes.

## Wiki Maintenance

```bash
python3 /root/.codex/skills/wiki-note/scripts/wiki.py rebuild --json
python3 /root/.codex/skills/wiki-note/scripts/wiki.py doctor --json
```

Run these after structural wiki edits or when README/AGENT links change.
