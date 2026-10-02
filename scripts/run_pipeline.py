import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from backend.etf_pipeline import ETFPipeline
from backend.backtest import Backtester

# 1. Load QQQ price data
price_df = pd.read_csv("data/QQQ.csv", parse_dates=["Date"], index_col="Date")

# 2. No news for now
headlines = []

# 3. Run pipeline daily
decisions = []
for date in price_df.index:
    daily_df = price_df.loc[:date]
    pipeline = ETFPipeline(daily_df, headlines)
    result = pipeline.run()
    decisions.append({"action": result["decision"]["action"]})


# 4. Backtest
bt = Backtester(price_df, decisions)
backtest_output = bt.run()

print("Final equity:", backtest_output["equity_curve"].iloc[-1])
print(result)
