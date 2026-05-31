---
title: Strategy Backtest And Execution
type: implementation
status: current
scope: quantdinger-strategy-runtime
last_checked: 2026-05-31
related_files:
  - backend_api_python/app/services/backtest.py
  - backend_api_python/app/services/backtest_execution.py
  - backend_api_python/app/services/trading_executor.py
  - backend_api_python/app/services/pending_order_worker.py
  - backend_api_python/app/services/live_trading
  - backend_api_python/app/services/strategy_script_runtime.py
  - backend_api_python/app/utils/safe_exec.py
source_docs:
  - docs/SIGNAL_EXECUTION_STANDARD.md
  - docs/SIGNAL_EXECUTION_STANDARD_CN.md
  - docs/STRATEGY_DEV_GUIDE.md
  - docs/STRATEGY_DEV_GUIDE_CN.md
  - docs/CROSS_SECTIONAL_STRATEGY_GUIDE_EN.md
  - docs/CROSS_SECTIONAL_STRATEGY_GUIDE_CN.md
  - docs/AI_TRADING_SYSTEM_PLAN_CN.md
tags:
  - strategy
  - backtest
  - execution
updated: 2026-05-31T15:25:00+08:00
---

# Strategy Backtest And Execution

## Scope

QuantDinger uses its own strategy runtime and backtest engine. It does not use
NautilusTrader, Backtrader, or vectorbt as the core execution layer.

This page owns current strategy signal semantics, simulation behavior, and the
boundary between signal generation and live order dispatch.

## Current Code Anchors

- `backend_api_python/app/routes/indicator.py`: indicator authoring and
  validation HTTP surface.
- `backend_api_python/app/routes/strategy.py`: strategy CRUD and lifecycle
  HTTP surface.
- `backend_api_python/app/routes/backtest.py`: backtest submission and result
  HTTP surface.
- `backend_api_python/app/routes/experiment.py`: experiment and tuning HTTP
  surface.
- `backend_api_python/app/services/indicator_workspace.py`: indicator
  persistence and authoring contract.
- `backend_api_python/app/services/indicator_params.py`: parameter parsing and
  indicator invocation helpers.
- `backend_api_python/app/services/backtest.py`: in-process simulation engine.
- `backend_api_python/app/services/backtest_execution.py`: execution helpers
  for strategy backtests.
- `backend_api_python/app/services/trading_executor.py`: live strategy signal
  provider.
- `backend_api_python/app/services/pending_order_worker.py`: pending-order
  dispatch worker.
- `backend_api_python/app/services/live_trading/`: direct REST live execution
  clients.
- `backend_api_python/app/services/strategy_script_runtime.py`: event-driven
  script strategy runtime.
- `backend_api_python/app/utils/safe_exec.py`: sandbox for user code.

## Strategy Forms

Supported strategy forms:

- `IndicatorStrategy`: vectorized dataframe code used for indicators, chart
  overlays, and backtest signals.
- `ScriptStrategy`: event-driven `on_init` / `on_bar` scripts using a `ctx`
  runtime object.
- Cross-sectional strategies: multi-symbol dataframe inputs that produce scores
  and rankings.

New strategy work should prefer an explicit signal contract rather than loose
`buy` / `sell` semantics. The recommended default is four-way signals:

- `open_long`
- `close_long`
- `open_short`
- `close_short`

Two-way `buy` / `sell` remains supported for simpler scripts, but it requires a
clear `tradeDirection` interpretation. Strategy code must not mix two-way and
four-way columns as competing fill drivers.

## Indicator Authoring Contract

Indicator code should be deterministic dataframe code. It may compute columns,
return parameterized outputs, and expose signals for charting/backtests. It
must not depend on filesystem access, network calls, process execution, hidden
global state, or raw credentials.

The safe path is:

1. validate generated code against the sandbox;
2. save the indicator to the workspace;
3. create or update a stopped strategy that references that indicator;
4. backtest;
5. only then consider signal/paper/live execution.

Generated code failures should be fixed in the generated strategy or by adding
a narrow reviewed runtime API. Do not weaken sandbox rules for convenience.

## Backtest Engine

`BacktestService` owns the in-process backtest engine:

1. Fetch market data through the data-source layer.
2. Execute indicator code through the safe execution sandbox.
3. Convert dataframe outputs into normalized signals.
4. Simulate fills, fees, slippage, liquidation, forced end-of-test exits, equity
   curve, and trades.
5. Persist backtest runs, trades, and equity points into PostgreSQL.

The current engine version is `strategy-backtest-v1`.

Strict mode maps live behavior to backtest behavior:

- Strict mode: confirmed closed-bar signal, next-bar-open fill.
- Non-strict mode: same-bar or high-precision crypto execution path when
  available.

High-precision crypto backtests can use finer execution timeframes such as
`1m`, `5m`, `15m`, or `30m` when the requested window stays within configured
data-size caps. Otherwise the engine falls back to standard candle backtesting.

Current high-precision workload caps are designed around roughly 25k execution
candles. Longer windows degrade to coarser precision or standard backtesting
rather than failing hard.

Persisted evidence should remain useful after the run:

- run type, strategy id/name, engine version, config snapshot, and code hash;
- normalized trade records with side, reason, payload, and balance;
- equity points for curve reconstruction;
- fee, slippage, liquidation, and forced end-of-test exit assumptions.

If fill semantics change, update tests and make the behavior visible in engine
version/config snapshots.

## Live Runtime

`TradingExecutor` is a signal provider. It manages strategy threads, fetches
price/K-line inputs, evaluates strategy code, deduplicates signals, and writes
pending order records.

It does not directly place exchange orders and does not use CCXT for order
submission.

`PendingOrderWorker` polls pending orders and dispatches live execution through
`app.services.live_trading`.

`app.services.live_trading` is a direct REST client layer. It intentionally
does not use CCXT. It contains per-exchange clients and a factory for Binance,
OKX, Bitget, Bybit, Coinbase Exchange, Kraken, KuCoin, Gate, Deepcoin, HTX,
IBKR, MT5, and Alpaca.

Live execution modes:

- `signal`: produce pending-order intent and notifications without live order
  placement.
- `paper`: record simulated/paper behavior where supported.
- `live`: submit orders only when explicitly enabled and configured.

`strict_mode=True` maps live signal evaluation toward backtest-like
closed-bar confirmation. `strict_mode=False` allows more aggressive intra-bar
entry behavior where supported by the strategy runtime.

## Worker And Safety Rules

- `TradingExecutor` must not directly place exchange orders.
- `PendingOrderWorker` must reclaim stale processing orders and respect
  position-sync cache/backoff settings.
- Position sync should avoid repeated exchange snapshots for strategies sharing
  the same credential.
- Fatal exchange errors should stop or protect the affected strategy rather
  than creating repeated live-order attempts.
- Strategy logs must be useful for UI diagnosis but must not contain secrets.
- Real-money trading checks require explicit operator authorization.

## Data Layer

Crypto market data uses CCXT for public OHLCV/ticker access. This use is
separate from live order submission. Data source code may bind CCXT instances
to the configured exchange and market type so charting, strategy signals, and
backtests observe the same venue family as live configuration.

## Sandbox Rules

Indicator and strategy code must run through `safe_exec.py` protections. The
sandbox blocks imports, file/network access, process execution, reflection
escape hatches, dangerous pandas/NumPy I/O, dunder traversal, and similar host
escape patterns.

Do not weaken sandbox rules to make generated strategy code pass. Fix the
strategy code or add a narrow, reviewed API surface.

## Migration Notes

For future Gravity/PVA integration, treat Gravity/PVA as first-class strategy
families rather than arbitrary user scripts. They can use QuantDinger's product
runtime, database, and Agent Gateway, but should keep typed parameter schemas,
research profiles, and promotion semantics rather than being flattened into
free-form indicator snippets.

## Verification

```bash
cd backend_api_python
pytest tests/test_backtest_execution.py tests/test_trading_execution_modes.py
pytest tests/test_agent_v1.py
python -m py_compile app/services/backtest.py
python -m py_compile app/services/trading_executor.py
python -m py_compile app/services/pending_order_worker.py
```

When behavior touches live clients, prefer paper/signal-mode checks unless the
user explicitly authorizes real broker actions.
