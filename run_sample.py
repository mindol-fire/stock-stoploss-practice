"""Run stoploss evaluator against sample_inputs.json and print a table."""

from __future__ import annotations

import json
from pathlib import Path

from stoploss_evaluator import evaluate_stock


def _fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def _fmt_price(value: float) -> str:
    return f"{value:.2f}"


def main() -> None:
    sample_path = Path(__file__).with_name("sample_inputs.json")
    sample_text = sample_path.read_text(encoding="utf-8")
    stocks = json.loads(sample_text)

    table_headers = [
        "ticker",
        "market",
        "rule",
        "stock_down",
        "index_down",
        "relative_down",
        "threshold_price",
        "status",
    ]

    rows: list[list[str]] = []
    for stock in stocks:
        result = evaluate_stock(stock)
        for rule in ("A", "B"):
            item = result[rule]
            rows.append(
                [
                    result["ticker"],
                    result["market"],
                    rule,
                    _fmt_pct(item["stock_down"]),
                    _fmt_pct(item["index_down"]),
                    _fmt_pct(item["relative_down"]),
                    _fmt_price(item["threshold_price"]),
                    item["status"],
                ]
            )

    widths = [len(h) for h in table_headers]
    for row in rows:
        for idx, col in enumerate(row):
            widths[idx] = max(widths[idx], len(col))

    def format_row(row: list[str]) -> str:
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))

    print(format_row(table_headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(format_row(row))


if __name__ == "__main__":
    main()
