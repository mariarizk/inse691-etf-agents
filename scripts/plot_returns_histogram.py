import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt

from backend.strategy import load_prices, run_strategy
from config import DATA_DIR

_, output = run_strategy(load_prices())

returns = output["returns"]

plt.figure(figsize=(12,6))
plt.hist(returns, bins=50, color="purple", alpha=0.7)
plt.title("MAS Daily Returns Distribution")
plt.grid(True)

plt.savefig(DATA_DIR / "returns_histogram.png")
plt.show()
