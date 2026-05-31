"""
API Routes Module — Agent Gateway + OpenAPI-registered human routes.
"""
from flask import Flask


def register_routes(app: Flask):
    """Register Agent Gateway and human web API (via flask-smorest)."""
    from app.openapi import init_openapi
    init_openapi(app)

    # Agent Gateway (/api/agent/v1) — versioned, scoped surface for AI agents.
    # See .codex/wiki/implementation/agent-gateway-and-mcp.md.
    from app.routes.agent_v1 import register as register_agent_v1
    register_agent_v1(app)
