---
title: Configuration And Integrations
type: reference
status: current
scope: quantdinger-config
last_checked: 2026-05-31
related_files:
  - backend_api_python/env.example
  - backend_api_python/app/routes/settings.py
  - backend_api_python/app/services/oauth_service.py
  - backend_api_python/app/services/usdt_payment
source_docs:
  - docs/OAUTH_CONFIG_EN.md
  - docs/OAUTH_CONFIG_CN.md
  - docs/NOTIFICATION_EMAIL_CONFIG_EN.md
  - docs/NOTIFICATION_EMAIL_CONFIG_CH.md
  - docs/NOTIFICATION_SMS_CONFIG_EN.md
  - docs/NOTIFICATION_SMS_CONFIG_CH.md
  - docs/NOTIFICATION_TELEGRAM_CONFIG_EN.md
  - docs/NOTIFICATION_TELEGRAM_CONFIG_CH.md
  - docs/USDT_PAYMENT_GUIDE.md
tags:
  - configuration
  - oauth
  - notifications
  - billing
updated: 2026-05-31T15:40:00+08:00
---

# Configuration And Integrations

## Scope

The canonical runtime configuration file is `backend_api_python/.env`, created
from `backend_api_python/env.example`.

## Required Settings

- `SECRET_KEY`: JWT signing and credential encryption root.
- `DATABASE_URL`: PostgreSQL connection string.
- `FRONTEND_URL`: canonical user-facing web origin.
- `ADMIN_USER` and `ADMIN_PASSWORD`: first admin bootstrap credentials.

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

## Billing And USDT Payments

USDT payment support can be enabled through env configuration. The current
payment model supports multiple chains, chain-specific receiving addresses,
explorer API keys, amount suffix disambiguation, expiration, and confirmation
polling.

Treat payment settings as production-sensitive. Test minimum payments before
accepting real users and keep watcher logs available for reconciliation.

Current payment model:

- each supported chain has one configured receiving address;
- orders are matched by unique amount suffix rather than per-order derived
  address;
- active orders must not collide on `(chain, amount_usdt)`;
- old xpub/per-order-address assumptions should not be restored without a
  deliberate migration.

## Agent Gateway Settings

Important env values:

- `AGENT_JOBS_MAX_WORKERS`: async agent job worker pool size.
- `AGENT_LIVE_TRADING_ENABLED`: hard kill switch for agent live trading.
- `QUANTDINGER_DEPLOYMENT_MODE`: `saas` or `hosted` forces hosted-mode guard.

For shared deployments, hosted mode should reject `T` scope token issuance and
force `paper_only=true`.

## Broker And Proxy Settings

Important env values:

- `ALLOW_LOCAL_DESKTOP_BROKERS`: controls IBKR/MT5 visibility on cloud/SaaS.
- `PROXY_URL`: exchange REST/CCXT egress proxy inside Docker.
- `LIVE_TRADING_CA_BUNDLE` / `LIVE_TRADING_SSL_VERIFY`: certificate behavior
  for exchange HTTPS.
- `SPOT_CLOSE_SAFETY_RATIO` and `SPOT_OPEN_QUOTE_BUFFER`: live spot sizing
  buffers.
- `POSITION_SYNC_ENABLED`, `POSITION_SYNC_INTERVAL_SEC`,
  `POSITION_SYNC_CACHE_TTL_SEC`, and `EXCHANGE_SYNC_BACKOFF_SEC`: exchange
  position sync behavior.

Do not assume host-level VPN/proxy state applies inside Docker containers.

## Verification

```bash
docker compose config
docker compose logs --tail=100 backend
curl -f http://localhost:5000/api/health
cd backend_api_python && pytest tests/test_usdt_payment_idempotency.py
```
