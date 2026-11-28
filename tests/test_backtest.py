import os
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from backend.backtest import Backtester
from backend.historic_backtest import (
    generate_daily_decisions,
    load_price_history,
    run_historic_backtest,
)
from backend.price_signals import risk_from_price, sentiment_from_price


class TestBacktester(unittest.TestCase):

    def setUp(self):
        self.price_df = load_price_history("data/QQQ.csv")
        self.decisions = [
            {"action": 1} for _ in range(len(self.price_df))
        ]

    def test_backtest_run(self):
        result = Backtester(self.price_df, self.decisions).run()

        self.assertIn("positions", result)
        self.assertIn("returns", result)
        self.assertIn("equity_curve", result)
        self.assertEqual(len(result["positions"]), len(self.price_df))
        self.assertEqual(len(result["returns"]), len(self.price_df))
        self.assertEqual(len(result["equity_curve"]), len(self.price_df))


class TestPriceSignals(unittest.TestCase):

    def setUp(self):
        self.price_df = load_price_history("data/QQQ.csv")

    def test_sentiment_from_price_labels(self):
        result = sentiment_from_price(self.price_df)
        self.assertIn(result["sentiment"], ["Positive", "Neutral", "Negative"])
        self.assertEqual(result["source"], "price")

    def test_risk_from_price_labels(self):
        result = risk_from_price(self.price_df)
        self.assertIn(result["risk"], ["Low", "Medium", "High"])
        self.assertEqual(result["source"], "price")


class TestHistoricBacktest(unittest.TestCase):

    def test_generate_daily_decisions_length(self):
        price_df = load_price_history("data/QQQ.csv")
        decisions = generate_daily_decisions(price_df)
        self.assertEqual(len(decisions), len(price_df))
        self.assertIn(decisions[-1]["action"], [-1, 0, 1])

    def test_run_historic_backtest_saves_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_historic_backtest(
                price_csv="data/QQQ.csv",
                data_dir=tmp,
                save_outputs=True,
            )
            self.assertIn("Total Return", result["metrics"])
            self.assertTrue(Path(tmp, "equity_curve.csv").exists())
            self.assertTrue(Path(tmp, "decisions.csv").exists())
            self.assertTrue(Path(tmp, "returns.csv").exists())


if __name__ == "__main__":
    unittest.main()
