import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt

from backend.metrics import compute_all_metrics
from backend.strategy import load_prices, run_strategy
from config import DATA_DIR

# -----------------------------
# 1. Run MAS pipeline daily + backtest
# -----------------------------
price_df = load_prices()
decisions, backtest_output = run_strategy(price_df)

equity = backtest_output["equity_curve"]
returns = backtest_output["returns"]

# -----------------------------
# 2. Save outputs
# -----------------------------
equity.to_csv(DATA_DIR / "equity_curve.csv")
returns.to_csv(DATA_DIR / "returns.csv")
pd.DataFrame(decisions, index=price_df.index).to_csv(DATA_DIR / "decisions.csv")

print("Saved equity_curve.csv, returns.csv, decisions.csv")

# -----------------------------
# 3. Compute metrics
# -----------------------------
metrics = compute_all_metrics(equity, returns)

print("\n=== MAS Strategy Performance Metrics ===\n")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")

# -----------------------------
# 4. Plot equity curve
# -----------------------------
plt.figure(figsize=(12,6))
plt.plot(equity, label="MAS Strategy Equity Curve", color="blue")
plt.title("MAS Strategy Equity Curve for QQQ")
plt.xlabel("Date")
plt.ylabel("Equity Value")
plt.legend()
plt.grid(True)

plt.savefig(DATA_DIR / "equity_curve.png")
print("Saved equity_curve.png")

plt.show()
