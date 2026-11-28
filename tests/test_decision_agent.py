import os
import sys
import unittest

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from agents.decision_agent import DecisionAgent


class TestDecisionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = DecisionAgent()

    def test_buy_when_all_aligned(self):
        result = self.agent.decide(
            "bullish",
            {
                "sentiment": "Positive",
                "confidence": 90,
                "reasoning": "Strong outlook.",
            },
            {
                "risk": "Low",
                "confidence": 85,
                "reasoning": "Stable market.",
            },
        )
        self.assertEqual(result["action"], 1)
        self.assertEqual(result["action_label"], "BUY")

    def test_sell_on_bearish_technical(self):
        result = self.agent.decide(
            "bearish",
            {
                "sentiment": "Positive",
                "confidence": 90,
                "reasoning": "Strong outlook.",
            },
            {
                "risk": "Low",
                "confidence": 85,
                "reasoning": "Stable market.",
            },
        )
        self.assertEqual(result["action"], -1)
        self.assertEqual(result["action_label"], "SELL")

    def test_low_confidence_sentiment_forced_neutral(self):
        result = self.agent.decide(
            "bullish",
            {
                "sentiment": "Positive",
                "confidence": 40,
                "reasoning": "Weak signal.",
            },
            {
                "risk": "Low",
                "confidence": 85,
                "reasoning": "Stable market.",
            },
        )
        self.assertEqual(result["action"], 0)
        self.assertEqual(result["action_label"], "HOLD")

    def test_invalid_technical_raises(self):
        with self.assertRaises(ValueError):
            self.agent.decide(
                "up",
                {"sentiment": "Positive", "confidence": 90, "reasoning": "x"},
                {"risk": "Low", "confidence": 85, "reasoning": "y"},
            )


if __name__ == "__main__":
    unittest.main()
