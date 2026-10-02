import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from backend.etf_pipeline import ETFPipeline
from backend.backtest import Backtester
from backend.metrics import compute_all_metrics

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

equity = backtest_output["equity_curve"]
returns = backtest_output["returns"]

# 5. Compute metrics
metrics = compute_all_metrics(equity, returns)

# 6. Print metrics
print("\n=== MAS Strategy Performance Metrics ===\n")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")
