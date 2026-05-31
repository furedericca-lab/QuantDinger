---
title: Broker And Market Guides
type: reference
status: current
scope: quantdinger-brokers
last_checked: 2026-06-01
related_files:
  - path: backend_api_python/app/services/live_trading
    role: owner
  - path: backend_api_python/app/services/live_trading/factory.py
    role: owner
  - path: backend_api_python/app/services/ibkr_trading
    role: owner
  - path: backend_api_python/app/services/mt5_trading
    role: owner
  - path: backend_api_python/app/services/alpaca_trading
    role: owner
  - path: backend_api_python/app/data_sources
    role: owner
  - path: backend_api_python/app/services/broker_market_policy.py
    role: owner
  - path: backend_api_python/app/utils/local_brokers.py
    role: config
code_anchors:
  - id: broker-live-client-factory
    kind: function
    file: backend_api_python/app/services/live_trading/factory.py
    symbol: create_client
    role: defines
  - id: broker-market-policy-validation
    kind: function
    file: backend_api_python/app/services/broker_market_policy.py
    symbol: validate_strategy_config
    role: defines
  - id: broker-local-desktop-guard
    kind: function
    file: backend_api_python/app/utils/local_brokers.py
    symbol: local_desktop_brokers_allowed
    role: explains
source_docs:
  - docs/IBKR_TRADING_GUIDE_EN.md
  - docs/MT5_TRADING_GUIDE_EN.md
  - docs/MT5_TRADING_GUIDE_CN.md
  - docs/INDICATOR_DEFINITIONS_CN.md
  - docs/FRONTEND_FAST_ANALYSIS.md
tags:
  - broker
  - market-data
  - ibkr
  - mt5
updated: 2026-06-01T00:15:00+08:00
---

# Broker And Market Guides

## Scope

QuantDinger supports crypto exchanges through direct REST clients and supports
traditional brokers through dedicated integrations.

This page owns broker and market-type assumptions. It should be checked before
changing symbol normalization, exchange clients, broker visibility, or
deployment rules around local desktop brokers.

## Current Code Anchors

- `backend_api_python/app/data_sources/`: public market data sources.
- `backend_api_python/app/services/live_trading/`: crypto live execution
  clients and symbol helpers.
- `backend_api_python/app/services/ibkr_trading/`: IBKR client and symbols.
- `backend_api_python/app/services/mt5_trading/`: MT5 client and symbols.
- `backend_api_python/app/services/alpaca_trading/`: Alpaca client and symbols.
- `backend_api_python/app/services/broker_market_policy.py`: broker/market
  policy behavior.
- `backend_api_python/app/utils/local_brokers.py`: local desktop broker
  availability controls.

## Crypto

Crypto market data uses the data-source layer and often CCXT for public OHLCV.
Live orders use direct REST clients under `app/services/live_trading`, not
CCXT.

Market type matters:

- `spot`: no short selling; close sizing must use free base balance and lot
  filters.
- `swap`: perpetual/futures behavior; reduce-only and position side handling
  depend on exchange.

Always verify symbol format for the selected exchange.

Crypto live clients currently include Binance, OKX, Bitget, Bybit, Coinbase
Exchange, Kraken, KuCoin, Gate, Deepcoin, and HTX families. Exchange-specific
symbol notation matters; examples include OKX swap `BASE/QUOTE:QUOTE` style and
Gate currency-pair formatting.

Position sync and order placement must respect exchange rate limits. Shared
credentials should reuse cached position snapshots where possible.

## IBKR

IBKR requires TWS or IB Gateway reachable from the backend host. In cloud or
SaaS deployments, local desktop brokers should be disabled unless a private
network bridge is explicitly supported.

Use a dedicated order `clientId` when live orders run alongside manual TWS/API
sessions, otherwise TWS may disconnect one of the sessions.

## MT5

MT5 requires the MetaTrader 5 terminal and is usually best run on Windows or a
host where the terminal is installed and reachable.

For public hosted deployments, MT5 should usually be hidden or disabled unless
the operator has built a private reachable terminal service.

## Alpaca

Alpaca supports US equities, ETFs, and crypto depending on account capability.
Use the paper flag and broker configuration explicitly.

Do not infer paper/live behavior from account name alone. Keep API base URL,
keys, and paper flag aligned.

## Fast Analysis

Fast analysis combines market data, indicators, optional external sentiment,
and LLM output. Frontend consumers must respect backend field semantics for
BUY/SELL, target prices, stop loss, future-period projections, and confidence.

## Market Data Rules

- Public OHLCV/ticker data may use CCXT for crypto.
- Data-source failures are not the same as live-order failures.
- CN/HK/US/forex/futures/regional sources may have different symbol formats
  and availability windows.
- `PROXY_URL` may be required from the backend process for exchange metadata
  and OHLCV even if browser access works.
- Certificate errors should be fixed with CA bundles where possible; disabling
  TLS verification is a last resort.

## Verification

```bash
uv run python -m py_compile backend_api_python/app/services/live_trading/factory.py
uv run python -m py_compile backend_api_python/app/services/pending_order_worker.py
uv run python -m py_compile backend_api_python/app/services/broker_market_policy.py
```

For live-order paths, use signal or paper mode unless the user explicitly
authorizes a real broker/account action.
