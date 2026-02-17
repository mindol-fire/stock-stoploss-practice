"""Rule-based stoploss evaluator for a single stock record."""

from __future__ import annotations

from typing import Dict

THRESHOLD_PERCENT = 10.0


def _down_percent(reference: float, current: float) -> float:
    """Return percent drawdown from reference to current."""
    return ((reference - current) / reference) * 100.0


def _status(stock_down: float, relative_down: float) -> str:
    """Return status based on stoploss rules."""
    if stock_down < THRESHOLD_PERCENT:
        return "OK"
    if relative_down >= THRESHOLD_PERCENT:
        return "HARD_STOP"
    return "MARKET_DRIVEN_ALERT"


def _evaluate_rule(
    *,
    base_price: float,
    close: float,
    base_index: float,
    index_close: float,
) -> Dict[str, float | str]:
    stock_down = _down_percent(base_price, close)
    index_down = _down_percent(base_index, index_close)
    relative_down = max(stock_down - index_down, 0.0)
    threshold_price = base_price * 0.90

    return {
        "stock_down": stock_down,
        "index_down": index_down,
        "relative_down": relative_down,
        "threshold_price": threshold_price,
        "status": _status(stock_down, relative_down),
    }


def evaluate_stock(stock: Dict[str, float | str]) -> Dict[str, Dict[str, float | str] | str]:
    """Evaluate one stock input against rule A/B.

    Expected fields:
    - ticker, market, index_symbol
    - entry_price, close, entry_index_ref, index_close
    - peak_price, peak_index_ref
    """
    close = float(stock["close"])
    index_close = float(stock["index_close"])

    rule_a = _evaluate_rule(
        base_price=float(stock["entry_price"]),
        close=close,
        base_index=float(stock["entry_index_ref"]),
        index_close=index_close,
    )
    rule_b = _evaluate_rule(
        base_price=float(stock["peak_price"]),
        close=close,
        base_index=float(stock["peak_index_ref"]),
        index_close=index_close,
    )

    return {
        "ticker": str(stock["ticker"]),
        "market": str(stock["market"]),
        "index_symbol": str(stock["index_symbol"]),
        "A": rule_a,
        "B": rule_b,
    }
