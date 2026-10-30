import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from agents.sentiment_agent import SentimentAgent


def prices(values):
    return pd.DataFrame({"Close": values}, index=pd.date_range("2025-01-01", periods=len(values)))


class TestSentimentAgent(unittest.TestCase):

    def setUp(self):
        self.agent = SentimentAgent()

    def test_strong_gain_is_positive(self):
        result = self.agent.analyze(prices([100, 102]))
        self.assertEqual(result["signal"], "positive")
        self.assertAlmostEqual(result["last_return"], 0.02)

    def test_strong_loss_is_negative(self):
        self.assertEqual(self.agent.analyze(prices([100, 98]))["signal"], "negative")

    def test_small_move_is_neutral(self):
        self.assertEqual(self.agent.analyze(prices([100, 100.5]))["signal"], "neutral")


if __name__ == "__main__":
    unittest.main()
