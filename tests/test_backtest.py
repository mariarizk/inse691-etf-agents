import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import unittest
import pandas as pd

from backend.backtest import Backtester


class TestBacktester(unittest.TestCase):

    def setUp(self):

        self.price_df = pd.read_csv(
            "data/QQQ.csv",
            parse_dates=["Date"],
            index_col="Date"
        )

        self.decisions = [
            {"action": 1}
            for _ in range(len(self.price_df))
        ]

    def test_backtest_run(self):

        bt = Backtester(
            self.price_df,
            self.decisions
        )

        result = bt.run()

        self.assertIn(
            "positions",
            result
        )

        self.assertIn(
            "returns",
            result
        )

        self.assertIn(
            "equity_curve",
            result
        )

        self.assertEqual(
            len(result["positions"]),
            len(self.price_df)
        )

        self.assertEqual(
            len(result["returns"]),
            len(self.price_df)
        )

        self.assertEqual(
            len(result["equity_curve"]),
            len(self.price_df)
        )

        print("\n=== Backtester Output ===\n")
        print(result["equity_curve"].tail())


if __name__ == "__main__":
    unittest.main()