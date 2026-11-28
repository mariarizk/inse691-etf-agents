"""Compare MAS equity curve vs QQQ buy-and-hold using historic data."""

import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import matplotlib.pyplot as plt

from backend.historic_backtest import run_historic_backtest


def main():
    result = run_historic_backtest(save_outputs=True)
    price_df = result["price_df"]
    mas_equity = result["backtest"]["equity_curve"]
    buyhold_equity = price_df["Close"] / price_df["Close"].iloc[0]

    plt.figure(figsize=(12, 6))
    plt.plot(mas_equity, label="MAS Strategy", color="blue")
    plt.plot(
        buyhold_equity,
        label="QQQ Buy-and-Hold",
        color="black",
        linestyle="--",
    )
    plt.title("MAS vs QQQ Buy-and-Hold")
    plt.grid(True)
    plt.legend()
    plt.savefig("data/mas_vs_buyhold.png")
    print("Saved data/mas_vs_buyhold.png")


if __name__ == "__main__":
    main()
