---
title: API Conventions
type: reference
status: current
scope: quantdinger-api-contracts
last_checked: 2026-06-01
related_files:
  - path: .codex/wiki/reference/api/openapi.yaml
    role: generated
  - path: .codex/wiki/reference/api/index.html
    role: generated
  - path: .codex/wiki/reference/agent/agent-openapi.json
    role: generated
  - path: backend_api_python/app/openapi/__init__.py
    role: owner
  - path: backend_api_python/app/openapi/routes
    role: owner
  - path: backend_api_python/app/openapi/schemas/common.py
    role: owner
  - path: backend_api_python/scripts/export_openapi.py
    role: tool
code_anchors:
  - id: api-openapi-init
    kind: function
    file: backend_api_python/app/openapi/__init__.py
    symbol: init_openapi
    role: defines
  - id: api-common-envelopes
    kind: schema
    file: backend_api_python/app/openapi/schemas/common.py
    symbol: HumanSuccessEnvelopeSchema
    role: defines
  - id: api-export-script
    kind: script
    file: backend_api_python/scripts/export_openapi.py
    symbol: export_spec
    role: references
source_docs:
  - .codex/wiki/reference/api/openapi.yaml
  - .codex/wiki/reference/api/index.html
  - .codex/wiki/reference/agent/agent-openapi.json
tags:
  - api
  - openapi
  - contracts
  - agent-gateway
updated: 2026-06-01T01:25:00+08:00
---

# API Conventions

This page is the durable contract reference for QuantDinger HTTP APIs.
Machine-readable API artifacts live inside the wiki:

| Spec | Path | Audience |
| --- | --- | --- |
| Human Web API (flask-smorest) | `.codex/wiki/reference/api/openapi.yaml` | Frontend, integrators, community |
| Human Web API ReDoc viewer | `.codex/wiki/reference/api/index.html` | Local browsing over HTTP |
| Agent Gateway | `.codex/wiki/reference/agent/agent-openapi.json` | AI agents, MCP, automation |

Browse the human spec locally by serving `.codex/wiki/reference/api/` over HTTP
and opening `index.html`. ReDoc cannot load `openapi.yaml` from a `file://`
URL because browsers block that same-origin request.

## Two API Surfaces

### Human Web API

The human API uses `/api/...` routes, browser/user JWT authentication, and the
legacy QuantDinger response envelope. It is the API surface used by the web and
mobile UI.

### Agent Gateway

The Agent Gateway uses `/api/agent/v1/...` routes and scoped agent tokens with
the `qd_agent_...` token shape. Keep the agent contract separate from the human
spec. Do not mix agent routes into the human OpenAPI document unless the
operation is explicitly marked with an `x-agent-only` tag.

The detailed Agent Gateway implementation notes live in
`implementation/agent-gateway-and-mcp.md`; the machine-readable agent contract
is `.codex/wiki/reference/agent/agent-openapi.json`.

## Response Envelopes

Human API success responses use:

```json
{
  "code": 1,
  "msg": "success",
  "data": {}
}
```

Human API errors use:

```json
{
  "code": 0,
  "msg": "Error description",
  "data": null
}
```

`code: 1` means success for the human API. The `msg` field is human-readable,
and `data` may be `null`.

Agent Gateway routes use `message`, not `msg`, and use `code: 0` on success.
Agent errors may include `details` and `retriable`; use
`.codex/wiki/reference/agent/agent-openapi.json` as the source of truth for
that surface.

Shared OpenAPI schemas for the human API include `HumanSuccessEnvelope`,
`HumanErrorEnvelope`, and `PaginationMeta` in the generated human spec.

## Authentication

| Scheme | Header | Used by |
| --- | --- | --- |
| `HumanJWT` | `Authorization: Bearer <jwt>` | Human Web API |
| `AgentToken` | `Authorization: Bearer qd_agent_...` | `/api/agent/v1/*` only |

JWTs are obtained through `POST /api/auth/login`. Agent tokens are managed by
Agent Gateway token routes and should be scoped narrowly.

## Visibility Tiers

Every operation migrated to flask-smorest should have an intentional visibility
classification:

| Tier | OpenAPI | Who may rely on it |
| --- | --- | --- |
| Public | default tag, no extension | Open-source community and third-party clients |
| Internal | `x-visibility: internal` | QuantDinger product code; may change without notice |
| Private | `x-visibility: private` | Admin or sensitive workflows with minimal public docs |

Migration priority for public modules: `market`, `indicator`, `backtest`,
`global-market`, and `health`.

Internal or sensitive modules include `strategy`, `credentials`,
`quick-trade`, and broker adapters such as `ibkr`, `alpaca`, and `mt5`.

## Naming And Versioning

- Paths use lowercase kebab-case segments such as `/api/global-market/...`.
- Query parameters use snake_case, such as `page_size` and `sort_by`.
- JSON bodies use snake_case to match the existing backend.
- Breaking changes must be called out in PR descriptions.
- Human API versioning should prefer `/api/v2/...` over silent breaking changes.

API behavior and committed specs should move together. Regenerate the human
OpenAPI file after changing documented human routes.

## Pagination

List endpoints should use this common shape inside `data`:

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 12
}
```

The OpenAPI schema name is `PaginationMeta`; fields may be inlined per route
during migration.

## Contributing API Changes

1. Implement new public human routes with flask-smorest in
   `backend_api_python/app/openapi/routes/`, or migrate the existing Blueprint
   into that package.
2. Regenerate the human spec with:

   ```bash
   cd backend_api_python
   python scripts/export_openapi.py
   ```

3. Commit the updated `.codex/wiki/reference/api/openapi.yaml` in the same
   change.
4. Update `.codex/wiki/reference/agent/agent-openapi.json` separately for
   Agent Gateway changes.
5. Include API contract impact and validation in the PR or task closeout.

Local interactive docs are available at `/api/docs/swagger` and
`/api/docs/redoc` when `OPENAPI_ENABLED=true` or `PYTHON_API_DEBUG=true`.

## Migration Status

| Module | Status | Spec source |
| --- | --- | --- |
| Health (`/`, `/health`, `/api/health`) | Migrated | flask-smorest |
| Agent Gateway | Hand-written OpenAPI plus CI lint | `.codex/wiki/reference/agent/agent-openapi.json` |
| All other modules | Legacy Flask Blueprint | Not yet in generated human OpenAPI |

The next migration phases should move `market` and other preserved public
modules incrementally into the flask-smorest OpenAPI package.
