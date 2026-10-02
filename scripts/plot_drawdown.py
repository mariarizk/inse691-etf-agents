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

equity = output["equity_curve"]

rolling_max = equity.cummax()
drawdown = (equity - rolling_max) / rolling_max

plt.figure(figsize=(12,6))
plt.plot(drawdown, color="red")
plt.title("MAS Strategy Drawdown")
plt.grid(True)

plt.savefig("data/drawdown.png")
plt.show()
