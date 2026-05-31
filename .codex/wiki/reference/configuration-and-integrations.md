---
title: Configuration And Integrations
type: reference
status: current
scope: quantdinger-config
last_checked: 2026-06-01
related_files:
  - path: backend_api_python/env.example
    role: config
  - path: backend_api_python/app/routes/settings.py
    role: owner
  - path: backend_api_python/app/services/oauth_service.py
    role: owner
  - path: backend_api_python/app/services/email_service.py
    role: caller
code_anchors:
  - id: quantdinger-settings-catalog
    kind: route
    file: backend_api_python/app/routes/settings.py
    symbol: settings_blp
    role: defines
  - id: quantdinger-oauth-service
    kind: class
    file: backend_api_python/app/services/oauth_service.py
    symbol: OAuthService
    role: defines
source_docs:
  - README.md
  - AGENT.md
tags:
  - configuration
  - oauth
  - notifications
updated: 2026-06-01T02:05:00+08:00
---

# Configuration And Integrations

## Scope

The canonical runtime configuration file is `backend_api_python/.env`, created
from `backend_api_python/env.example`.

This checkout has no billing, USDT payment, credits, VIP, membership, or
community marketplace configuration. Do not restore those env groups during
upstream sync unless the product baseline changes explicitly.

## Required Settings

- `SECRET_KEY`: JWT signing and credential encryption root.
- `DATABASE_URL` or `POSTGRES_*`: PostgreSQL connection settings.
- `REDIS_HOST` and `REDIS_PORT`: Redis cache/coordination settings.
- `FRONTEND_URL`: canonical user-facing web origin.
- `ADMIN_USER`, `ADMIN_PASSWORD`, and `ADMIN_EMAIL`: first admin bootstrap
  credentials.

Also review `ENABLE_REGISTRATION`, `OAUTH_ALLOWED_REDIRECTS`,
`SKIP_AUTO_MIGRATE`, database pool settings, route-level executor workers, and
Gunicorn worker/thread settings before production use.

## LLM Providers

`LLM_PROVIDER` chooses the active provider. Supported env families include
OpenRouter, OpenAI, Google, DeepSeek, Grok, custom OpenAI-compatible APIs, and
MiniMax. Never commit provider keys.

LLM use appears in fast analysis, AI chat, code generation, and AI-assisted
optimization flows. Expensive or model-calling agent operations should require
an explicit confirmation flag.

## OAuth And Signup Controls

OAuth supports Google and GitHub when configured through env values. Keep
redirect URLs aligned with `FRONTEND_URL` and `OAUTH_ALLOWED_REDIRECTS`.

Cloudflare Turnstile can be used for bot protection. User registration can be
enabled or disabled with `ENABLE_REGISTRATION`.

OAuth state is stored in PostgreSQL so multi-worker deployments do not lose
CSRF state between callback and login request.

## Notifications

Notification channels include email via SMTP, SMS via Twilio, and Telegram bot
notifications. Notification credentials must remain in environment or encrypted
settings. Strategy code should request notification behavior through product
settings, not embed raw tokens.

Notification channels can be used by strategy signals, login/security events,
and product workflows. Keep credentials out of strategy code and wiki examples.

## Agent Gateway Settings

Important env values:

- `AGENT_JOBS_MAX_WORKERS`: async agent job worker pool size.
- `AGENT_LIVE_TRADING_ENABLED`: hard kill switch for agent live trading.
- `QUANTDINGER_DEPLOYMENT_MODE`: `saas` or `hosted` forces hosted-mode guard.

For shared deployments, hosted mode should reject `T` scope token issuance and
force `paper_only=true`.

## Broker And Proxy Settings

Important env values:

- `ALLOW_LOCAL_DESKTOP_BROKERS`: controls IBKR/MT5 visibility on hosted use.
- `PROXY_URL`: exchange REST/CCXT egress proxy from the backend process.
- `LIVE_TRADING_CA_BUNDLE` / `LIVE_TRADING_SSL_VERIFY`: certificate behavior
  for exchange HTTPS.
- `SPOT_CLOSE_SAFETY_RATIO` and `SPOT_OPEN_QUOTE_BUFFER`: live spot sizing
  buffers.
- `POSITION_SYNC_ENABLED`, `POSITION_SYNC_INTERVAL_SEC`,
  `POSITION_SYNC_CACHE_TTL_SEC`, and `EXCHANGE_SYNC_BACKOFF_SEC`: exchange
  position sync behavior.

Do not assume browser network success proves backend exchange egress.

## Verification

```bash
curl -f http://127.0.0.1:5000/api/health
uv run python -m pytest backend_api_python/tests/test_health.py
uv run python -m pytest backend_api_python/tests/test_agent_v1.py backend_api_python/tests/test_agent_v1_saas_guard.py
```
