import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.metrics import compute_all_metrics
from backend.strategy import load_prices, run_strategy

_, backtest_output = run_strategy(load_prices())

metrics = compute_all_metrics(backtest_output["equity_curve"], backtest_output["returns"])

print("\n=== MAS Strategy Performance Metrics ===\n")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")
