import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import matplotlib.pyplot as plt

from backend.historic_backtest import run_historic_backtest


result = run_historic_backtest(save_outputs=True)
equity = result["backtest"]["equity_curve"]
drawdown = (equity - equity.cummax()) / equity.cummax()

plt.figure(figsize=(12, 6))
plt.plot(drawdown, color="red")
plt.title("MAS Strategy Drawdown")
plt.grid(True)
plt.savefig("data/drawdown.png")
print("Saved data/drawdown.png")
