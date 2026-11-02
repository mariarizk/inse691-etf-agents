import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from agents.technical_agent import TechnicalAgent


def prices(values):
    return pd.DataFrame({"Close": values}, index=pd.date_range("2025-01-01", periods=len(values)))


class TestTechnicalAgent(unittest.TestCase):

    def setUp(self):
        self.agent = TechnicalAgent()

    def test_uptrend_is_bullish(self):
        result = self.agent.analyze(prices([100 + i for i in range(40)]))
        self.assertEqual(result["signal"], "bullish")
        self.assertGreater(result["short_ma"], result["long_ma"])

    def test_downtrend_is_bearish(self):
        result = self.agent.analyze(prices([200 - i for i in range(40)]))
        self.assertEqual(result["signal"], "bearish")

    def test_flat_market_is_neutral(self):
        result = self.agent.analyze(prices([100.0] * 40))
        self.assertEqual(result["signal"], "neutral")


if __name__ == "__main__":
    unittest.main()
