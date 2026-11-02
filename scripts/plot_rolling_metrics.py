import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt

from backend.strategy import load_prices, run_strategy
from config import DATA_DIR

_, output = run_strategy(load_prices())

returns = output["returns"]

rolling_vol = returns.rolling(30).std() * np.sqrt(252)

risk_free = 0.02 / 252
rolling_sharpe = ((returns.rolling(30).mean() - risk_free) /
                  returns.rolling(30).std()) * np.sqrt(252)

plt.figure(figsize=(12,6))
plt.plot(rolling_vol, color="orange")
plt.title("Rolling Volatility (30-day)")
plt.grid(True)
plt.savefig(DATA_DIR / "rolling_volatility.png")
plt.show()

plt.figure(figsize=(12,6))
plt.plot(rolling_sharpe, color="green")
plt.title("Rolling Sharpe Ratio (30-day)")
plt.grid(True)
plt.savefig(DATA_DIR / "rolling_sharpe.png")
plt.show()
