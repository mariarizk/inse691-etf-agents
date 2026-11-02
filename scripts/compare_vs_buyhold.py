import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt

from backend.strategy import buy_and_hold, load_prices, run_strategy
from config import DATA_DIR

price_df = load_prices()
_, output = run_strategy(price_df)

mas_equity = output["equity_curve"]
buyhold_equity = buy_and_hold(price_df)["equity_curve"]

plt.figure(figsize=(12,6))
plt.plot(mas_equity, label="MAS Strategy", color="blue")
plt.plot(buyhold_equity, label="QQQ Buy-and-Hold", color="black", linestyle="--")
plt.title("MAS vs QQQ Buy-and-Hold")
plt.grid(True)
plt.legend()

plt.savefig(DATA_DIR / "mas_vs_buyhold.png")
plt.show()
