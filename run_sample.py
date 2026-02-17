"""
Run stoploss evaluator against sample_inputs.json and print a table.
"""

from __future__ import annotations

import json
from pathlib import Path

from stoploss_evaluator_clean import evaluate_stock


def fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def fmt_price(value: float) -> str:
    return f"{value:.2f}"


def main() -> None:
    sample_path = Path(__file__).with_name("sample_inputs.json")
    stocks = json.loads(sample_path.read_text(encoding="utf-8"))

    headers = [
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
                    fmt_pct(float(item["stock_down"])),
                    fmt_pct(float(item["index_down"])),
                    fmt_pct(float(item["relative_down"])),
                    fmt_price(float(item["threshold_price"])),
                    str(item["status"]),
                ]
            )

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def format_row(row: list[str]) -> str:
        return " | ".join(row[i].ljust(widths[i]) for i in range(len(headers)))

    print(format_row(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(format_row(row))


if __name__ == "__main__":
    main()
