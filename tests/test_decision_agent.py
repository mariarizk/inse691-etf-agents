import unittest

from agents.decision_agent import DecisionAgent


class TestDecisionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = DecisionAgent()

    def test_buy_signal(self):

        technical = "bullish"

        sentiment = {
            "sentiment": "Positive",
            "confidence": 90,
            "reasoning": "Strong earnings."
        }

        risk = {
            "risk": "Low",
            "confidence": 85,
            "reasoning": "Low volatility."
        }

        result = self.agent.decide(
            technical,
            sentiment,
            risk
        )

        self.assertEqual(result["action"], 1)

    def test_sell_signal(self):

        technical = "bearish"

        sentiment = {
            "sentiment": "Negative",
            "confidence": 95,
            "reasoning": "Weak outlook."
        }

        risk = {
            "risk": "High",
            "confidence": 90,
            "reasoning": "Regulatory concerns."
        }

        result = self.agent.decide(
            technical,
            sentiment,
            risk
        )

        self.assertEqual(result["action"], -1)

    def test_hold_signal(self):

        technical = "bullish"

        sentiment = {
            "sentiment": "Positive",
            "confidence": 90,
            "reasoning": "Positive article."
        }

        risk = {
            "risk": "Medium",
            "confidence": 80,
            "reasoning": "Moderate risk."
        }

        result = self.agent.decide(
            technical,
            sentiment,
            risk
        )

        self.assertEqual(result["action"], 0)

    def test_low_confidence_sentiment(self):

        technical = "bullish"

        sentiment = {
            "sentiment": "Positive",
            "confidence": 40,
            "reasoning": "Weak confidence."
        }

        risk = {
            "risk": "Low",
            "confidence": 90,
            "reasoning": "Stable market."
        }

        result = self.agent.decide(
            technical,
            sentiment,
            risk
        )

        self.assertEqual(result["action"], 0)


if __name__ == "__main__":
    unittest.main()