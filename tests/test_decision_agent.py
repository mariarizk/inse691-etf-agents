import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.blackboard import Blackboard
from agents.decision_agent import DecisionAgent


class TestDecisionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = DecisionAgent()

    def test_buy_signal(self):
        sentiment = {"sentiment": "Positive", "confidence": 90, "reasoning": "Strong earnings."}
        risk = {"risk": "Low", "confidence": 85, "reasoning": "Low volatility."}

        result = self.agent.decide("bullish", sentiment, risk)

        self.assertEqual(result["action"], 1)
        self.assertEqual(result["label"], "BUY")

    def test_sell_signal(self):
        sentiment = {"sentiment": "Negative", "confidence": 95, "reasoning": "Weak outlook."}
        risk = {"risk": "High", "confidence": 90, "reasoning": "Regulatory concerns."}

        self.assertEqual(self.agent.decide("bearish", sentiment, risk)["action"], -1)

    def test_hold_signal(self):
        sentiment = {"sentiment": "Positive", "confidence": 90, "reasoning": "Positive article."}
        risk = {"risk": "Medium", "confidence": 80, "reasoning": "Moderate risk."}

        result = self.agent.decide("bullish", sentiment, risk)

        self.assertEqual(result["action"], 0)
        self.assertIn("Mixed signals", result["reasoning"])

    def test_low_confidence_sentiment(self):
        sentiment = {"sentiment": "Positive", "confidence": 40, "reasoning": "Weak confidence."}
        risk = {"risk": "Low", "confidence": 90, "reasoning": "Stable market."}

        self.assertEqual(self.agent.decide("bullish", sentiment, risk)["action"], 0)

    def test_low_confidence_high_risk_is_ignored(self):
        sentiment = {"sentiment": "Positive", "confidence": 90, "reasoning": "Good news."}
        risk = {"risk": "High", "confidence": 30, "reasoning": "Unclear."}

        self.assertEqual(self.agent.decide("bullish", sentiment, risk)["action"], 0)

    def test_reads_signals_from_blackboard(self):
        board = Blackboard()
        board.write("technical", {"signal": "bullish"})
        board.write("sentiment", {"sentiment": "Positive", "confidence": 90})
        board.write("risk", {"risk": "Low", "confidence": 90})

        self.assertEqual(self.agent.decide_from_blackboard(board)["label"], "BUY")


if __name__ == "__main__":
    unittest.main()
