import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt

from backend.strategy import load_prices, run_strategy
from config import DATA_DIR

_, output = run_strategy(load_prices())

equity = output["equity_curve"]

plt.figure(figsize=(12,6))
plt.plot(equity, label="MAS Equity Curve", color="blue")
plt.title("MAS Strategy Equity Curve")
plt.grid(True)
plt.legend()

plt.savefig(DATA_DIR / "equity_curve.png")
plt.show()
