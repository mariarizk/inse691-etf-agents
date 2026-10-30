import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from agents.risk_agent import RiskAgent


def prices(daily_returns):
    values = [100.0]
    for ret in daily_returns:
        values.append(values[-1] * (1 + ret))
    return pd.DataFrame({"Close": values}, index=pd.date_range("2025-01-01", periods=len(values)))


class TestRiskAgent(unittest.TestCase):

    def setUp(self):
        self.agent = RiskAgent()

    def test_calm_market_is_low_risk(self):
        result = self.agent.analyze(prices([0.002, -0.002] * 15))
        self.assertEqual(result["signal"], "low")
        self.assertLess(result["daily_volatility"], 0.01)

    def test_moderate_swings_are_medium_risk(self):
        self.assertEqual(self.agent.analyze(prices([0.015, -0.015] * 15))["signal"], "medium")

    def test_large_swings_are_high_risk(self):
        self.assertEqual(self.agent.analyze(prices([0.05, -0.05] * 15))["signal"], "high")


if __name__ == "__main__":
    unittest.main()
