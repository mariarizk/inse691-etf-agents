import os
import sys
import unittest

import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from agents.technical_agent import TechnicalAgent


class TestTechnicalAgent(unittest.TestCase):

    def setUp(self):
        self.agent = TechnicalAgent()
        closes = (
            [100 + i * 0.5 for i in range(40)]
            + [120 - i for i in range(40)]
        )
        self.price_df = pd.DataFrame(
            {"Close": closes},
            index=pd.date_range("2025-01-01", periods=len(closes), freq="B"),
        )

    def test_returns_allowed_labels(self):
        label = self.agent.analyze(self.price_df)
        self.assertIn(label, ["bullish", "bearish", "neutral"])

    def test_bullish_when_short_ma_above_long_ma(self):
        rising = pd.DataFrame(
            {"Close": [100 + i for i in range(40)]},
            index=pd.date_range("2025-01-01", periods=40, freq="B"),
        )
        self.assertEqual(self.agent.analyze(rising), "bullish")

    def test_bearish_when_short_ma_below_long_ma(self):
        falling = pd.DataFrame(
            {"Close": [140 - i for i in range(40)]},
            index=pd.date_range("2025-01-01", periods=40, freq="B"),
        )
        self.assertEqual(self.agent.analyze(falling), "bearish")


if __name__ == "__main__":
    unittest.main()
