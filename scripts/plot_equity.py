import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import matplotlib.pyplot as plt

from backend.historic_backtest import run_historic_backtest


result = run_historic_backtest(save_outputs=True)
equity = result["backtest"]["equity_curve"]

plt.figure(figsize=(12, 6))
plt.plot(equity, label="MAS Equity Curve", color="blue")
plt.title("MAS Strategy Equity Curve")
plt.grid(True)
plt.legend()
plt.savefig("data/equity_curve.png")
print("Saved data/equity_curve.png")
