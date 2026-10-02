import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt

from backend.etf_pipeline import ETFPipeline
from backend.backtest import Backtester

price_df = pd.read_csv("data/QQQ.csv", parse_dates=["Date"], index_col="Date")

headlines = []
decisions = []

for date in price_df.index:
    daily_df = price_df.loc[:date]
    pipeline = ETFPipeline(daily_df, headlines)
    result = pipeline.run()
    decisions.append({"action": result["decision"]["action"]})


bt = Backtester(price_df, decisions)
output = bt.run()

mas_equity = output["equity_curve"]
buyhold_equity = price_df["Close"] / price_df["Close"].iloc[0]

plt.figure(figsize=(12,6))
plt.plot(mas_equity, label="MAS Strategy", color="blue")
plt.plot(buyhold_equity, label="QQQ Buy-and-Hold", color="black", linestyle="--")
plt.title("MAS vs QQQ Buy-and-Hold")
plt.grid(True)
plt.legend()

plt.savefig("data/mas_vs_buyhold.png")
plt.show()
