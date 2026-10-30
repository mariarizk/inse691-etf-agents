import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt

from backend.strategy import load_prices, run_strategy
from config import DATA_DIR

_, output = run_strategy(load_prices())

equity = output["equity_curve"]

rolling_max = equity.cummax()
drawdown = (equity - rolling_max) / rolling_max

plt.figure(figsize=(12,6))
plt.plot(drawdown, color="red")
plt.title("MAS Strategy Drawdown")
plt.grid(True)

plt.savefig(DATA_DIR / "drawdown.png")
plt.show()
