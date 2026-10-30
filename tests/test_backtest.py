import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from backend.backtest import Backtester


class TestBacktester(unittest.TestCase):

    def setUp(self):
        self.price_df = pd.DataFrame(
            {"Close": [100.0, 110.0, 99.0, 99.0]},
            index=pd.date_range("2025-01-01", periods=4),
        )

    def test_position_applies_to_next_day_return(self):
        decisions = [{"action": 1}, {"action": -1}, {"action": 0}, {"action": 0}]
        returns = Backtester(self.price_df, decisions).run()["returns"]

        self.assertAlmostEqual(returns.iloc[0], 0.0)
        self.assertAlmostEqual(returns.iloc[1], 0.10)
        self.assertAlmostEqual(returns.iloc[2], 0.10)
        self.assertAlmostEqual(returns.iloc[3], 0.0)

    def test_equity_curve_compounds_returns(self):
        decisions = [{"action": 1}] * 4
        equity = Backtester(self.price_df, decisions).run()["equity_curve"]

        self.assertAlmostEqual(equity.iloc[-1], 0.99)


if __name__ == "__main__":
    unittest.main()
