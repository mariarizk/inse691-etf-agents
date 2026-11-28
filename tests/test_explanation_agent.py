import os
import sys
import unittest

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from agents.explanation_agent import ExplanationAgent


class TestExplanationAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ExplanationAgent()
        self.technical = "bullish"
        self.sentiment = {
            "sentiment": "Positive",
            "confidence": 88,
            "reasoning": "Strong earnings growth.",
        }
        self.risk = {
            "risk": "Low",
            "confidence": 84,
            "reasoning": "Low volatility.",
        }
        self.decision = {
            "action": 1,
            "action_label": "BUY",
            "reasoning": "Aligned bullish signals.",
        }

    def test_analyze_returns_explanation(self):
        result = self.agent.analyze(
            self.technical,
            self.sentiment,
            self.risk,
            self.decision,
        )
        self.assertIn("explanation", result)
        self.assertGreater(len(result["explanation"]), 20)
        self.assertIn("consistency", result)
        self.assertIn(result["consistency"], [True, False])


if __name__ == "__main__":
    unittest.main()
