"""Run historic MAS backtest on collected QQQ.csv data.

Default (design-spec): price rules only, no Gemini calls.
Optional LLM news days:
  python scripts/run_backtest.py --news data/news_history.csv --llm-news
"""

import argparse
import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import matplotlib.pyplot as plt

from backend.historic_backtest import run_historic_backtest


def parse_args():
    parser = argparse.ArgumentParser(
        description="Historic QQQ multi-agent backtest"
    )
    parser.add_argument(
        "--price",
        default="data/QQQ.csv",
        help="Historic price CSV (Date, Close)",
    )
    parser.add_argument(
        "--news",
        default=None,
        help="Optional news CSV (Date, article) for LLM days",
    )
    parser.add_argument(
        "--llm-news",
        action="store_true",
        help="Use ETFPipeline/LLM for days that have news text",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    result = run_historic_backtest(
        price_csv=args.price,
        news_csv=args.news,
        use_llm_news=args.llm_news,
        save_outputs=True,
    )

    equity = result["backtest"]["equity_curve"]
    metrics = result["metrics"]

    print("\n=== MAS Strategy Performance Metrics ===\n")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

    plt.figure(figsize=(12, 6))
    plt.plot(equity, label="MAS Strategy Equity Curve", color="blue")
    plt.title("MAS Strategy Equity Curve for QQQ")
    plt.xlabel("Date")
    plt.ylabel("Equity Value")
    plt.legend()
    plt.grid(True)
    plt.savefig("data/equity_curve.png")
    print("\nSaved data/equity_curve.csv, returns.csv, decisions.csv, equity_curve.png")


if __name__ == "__main__":
    main()
