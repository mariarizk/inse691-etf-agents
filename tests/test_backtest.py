import sys, os

# Add project root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.backtest import Backtester

bt = Backtester("QQQ", "2018-01-01", "2024-01-01")

df = bt.run()
df = bt.compute_performance(df)

bt.save_results(df)
bt.plot_results(df)
