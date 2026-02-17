"""
Rule-based stoploss evaluator for a single stock record.
"""

from __future__ import annotations

from typing import Any, Dict, Union


def evaluate_rule(
    *,
    base_price: float,
    close: float,
    base_index: float,
    index_close: float,
    stop_pct: float = 10.0,
) -> Dict[str, Union[float, str]]:
    stock_down = max(0.0, ((base_price - close) / base_price) * 100.0)
    index_down = max(0.0, ((base_index - index_close) / base_index) * 100.0)
    relative_down = max(0.0, stock_down - index_down)
    threshold_price = base_price * (1.0 - stop_pct / 100.0)

    if stock_down < stop_pct:
        status = "OK"
    elif relative_down >= stop_pct:
        status = "HARD_STOP"
    else:
        status = "MARKET_DRIVEN_ALERT"

    return {
        "stock_down": stock_down,
        "index_down": index_down,
        "relative_down": relative_down,
        "threshold_price": threshold_price,
        "status": status,
    }


def evaluate_stock(stock: Dict[str, Any]) -> Dict[str, Any]:
    close = float(stock["close"])
    index_close = float(stock["index_close"])

    rule_a = evaluate_rule(
        base_price=float(stock["entry_price"]),
        close=close,
        base_index=float(stock["entry_index_ref"]),
        index_close=index_close,
    )

    rule_b = evaluate_rule(
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
