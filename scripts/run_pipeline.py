import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.etf_pipeline import ETFPipeline
from backend.strategy import load_prices, run_strategy

price_df = load_prices()
_, backtest_output = run_strategy(price_df)

print("Final equity:", backtest_output["equity_curve"].iloc[-1])
print("Latest blackboard:", ETFPipeline().run(price_df))
