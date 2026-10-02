import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt

from backend.etf_pipeline import ETFPipeline
from backend.backtest import Backtester
from backend.metrics import compute_all_metrics

# -----------------------------
# 1. Load QQQ price data
# -----------------------------

price_df = pd.read_csv("data/QQQ.csv", parse_dates=["Date"], index_col="Date")
print(price_df.columns)

# -----------------------------
# 2. Load news (optional)
# -----------------------------
headlines = []  # no news for now

# -----------------------------
# 3. Run MAS pipeline daily
# -----------------------------
decisions = []
for date in price_df.index:
    daily_df = price_df.loc[:date]
    pipeline = ETFPipeline(daily_df, headlines)
    result = pipeline.run()
    decisions.append({"action": result["decision"]["action"]})


# -----------------------------
# 4. Backtest
# -----------------------------
bt = Backtester(price_df, decisions)
backtest_output = bt.run()

equity = backtest_output["equity_curve"]
returns = backtest_output["returns"]

# -----------------------------
# 5. Save outputs
# -----------------------------
equity.to_csv("data/equity_curve.csv")
returns.to_csv("data/returns.csv")

pd.DataFrame({"decision": decisions}, index=price_df.index).to_csv("data/decisions.csv")

print("Saved equity_curve.csv, returns.csv, decisions.csv")

# -----------------------------
# 6. Compute metrics
# -----------------------------
metrics = compute_all_metrics(equity, returns)

print("\n=== MAS Strategy Performance Metrics ===\n")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")

# -----------------------------
# 7. Plot equity curve
# -----------------------------
plt.figure(figsize=(12,6))
plt.plot(equity, label="MAS Strategy Equity Curve", color="blue")
plt.title("MAS Strategy Equity Curve for QQQ")
plt.xlabel("Date")
plt.ylabel("Equity Value")
plt.legend()
plt.grid(True)

plt.savefig("data/equity_curve.png")
print("Saved equity_curve.png")

plt.show()
