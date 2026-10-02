import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
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

returns = output["returns"]

rolling_vol = returns.rolling(30).std() * np.sqrt(252)

risk_free = 0.02 / 252
rolling_sharpe = ((returns.rolling(30).mean() - risk_free) /
                  returns.rolling(30).std()) * np.sqrt(252)

plt.figure(figsize=(12,6))
plt.plot(rolling_vol, color="orange")
plt.title("Rolling Volatility (30-day)")
plt.grid(True)
plt.savefig("data/rolling_volatility.png")
plt.show()

plt.figure(figsize=(12,6))
plt.plot(rolling_sharpe, color="green")
plt.title("Rolling Sharpe Ratio (30-day)")
plt.grid(True)
plt.savefig("data/rolling_sharpe.png")
plt.show()
