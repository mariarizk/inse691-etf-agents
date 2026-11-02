import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from agents.llm_client import LlmError
from agents.risk_agent import RiskAgent

ARTICLE = """
NVIDIA shares fell after regulators announced a new review
of AI chip exports to foreign markets. Analysts expect
additional restrictions to impact future revenue growth.
"""


def prices(daily_returns):
    values = [100.0]
    for ret in daily_returns:
        values.append(values[-1] * (1 + ret))
    return pd.DataFrame({"Close": values}, index=pd.date_range("2025-01-01", periods=len(values)))


class FakeLlm:
    def __init__(self, reply=None, error=None):
        self.reply = reply
        self.error = error
        self.prompts = []

    def complete_json(self, system_prompt, user_prompt):
        self.prompts.append(user_prompt)
        if self.error:
            raise self.error
        return self.reply


class TestRiskAgent(unittest.TestCase):

    def test_classifies_news_with_llm_and_volatility(self):
        llm = FakeLlm({"risk": "high", "confidence": 92, "reasoning": "Regulatory review."})
        result = RiskAgent(llm).analyze(prices([0.002, -0.002] * 15), ARTICLE)

        self.assertEqual(result["risk"], "High")
        self.assertEqual(result["confidence"], 92)
        self.assertEqual(result["source"], "llm")
        self.assertIn("20-day volatility", llm.prompts[0])

    def test_calm_market_without_news_is_low_risk(self):
        result = RiskAgent().analyze(prices([0.002, -0.002] * 15))

        self.assertEqual(result["risk"], "Low")
        self.assertEqual(result["source"], "price")
        self.assertLess(result["daily_volatility"], 0.01)

    def test_moderate_swings_without_news_are_medium_risk(self):
        self.assertEqual(RiskAgent().analyze(prices([0.015, -0.015] * 15))["risk"], "Medium")

    def test_large_swings_without_news_are_high_risk(self):
        self.assertEqual(RiskAgent().analyze(prices([0.05, -0.05] * 15))["risk"], "High")

    def test_falls_back_to_volatility_when_llm_fails(self):
        result = RiskAgent(FakeLlm(error=LlmError("timeout"))).analyze(prices([0.05, -0.05] * 15), ARTICLE)

        self.assertEqual(result["risk"], "High")
        self.assertEqual(result["source"], "price")
        self.assertIn("timeout", result["reasoning"])


if __name__ == "__main__":
    unittest.main()
