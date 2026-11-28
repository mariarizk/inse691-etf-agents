import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import matplotlib.pyplot as plt

from backend.historic_backtest import run_historic_backtest


result = run_historic_backtest(save_outputs=True)
returns = result["backtest"]["returns"]

plt.figure(figsize=(12, 6))
plt.hist(returns, bins=50, color="purple", alpha=0.7)
plt.title("MAS Daily Returns Distribution")
plt.grid(True)
plt.savefig("data/returns_histogram.png")
print("Saved data/returns_histogram.png")
