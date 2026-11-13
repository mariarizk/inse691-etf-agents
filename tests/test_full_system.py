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

from backend.etf_pipeline import ETFPipeline
from backend.backtest import Backtester


class TestFullSystem(unittest.TestCase):

    def test_end_to_end(self):

        price_df = pd.read_csv(
            "data/QQQ.csv",
            parse_dates=["Date"],
            index_col="Date"
        )

        article = """
        Microsoft reported stronger-than-expected earnings
        and raised guidance for next quarter.
        """

        pipeline = ETFPipeline()

        output = pipeline.run(
            price_df,
            article
        )

        decision = output["decision"]

        decisions = [
            {
                "action": decision["action"]
            }
            for _ in range(len(price_df))
        ]

        bt = Backtester(
            price_df,
            decisions
        )

        backtest_output = bt.run()

        self.assertIn(
            "equity_curve",
            backtest_output
        )

        print("\n=== End-to-End Test PASS ===")


if __name__ == "__main__":
    unittest.main()