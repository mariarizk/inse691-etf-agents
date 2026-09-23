import sys, os
import unittest

# Add project root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from agents.decision_agent import DecisionAgent

class TestDecisionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = DecisionAgent()

        self.mock_fundamental = {"score": 3}
        self.mock_technical_buy = {"signal": "BUY"}
        self.mock_technical_sell = {"signal": "SELL"}
        self.mock_technical_hold = {"signal": "HOLD"}

        self.mock_risk_low = {"risk_score": 2}
        self.mock_risk_high = {"risk_score": 5}

        self.mock_sentiment_positive = {"sentiment_score": 1}
        self.mock_sentiment_negative = {"sentiment_score": -1}

        self.mock_diversification = {"score": 2}

    def test_buy_signal(self):
        mock_debate = {
            "bullish_arguments": ["Strong momentum"],
            "bearish_arguments": [],
            "conflicts": []
        }

        result = self.agent.decide(
            self.mock_fundamental,
            self.mock_technical_buy,
            self.mock_risk_low,
            self.mock_sentiment_positive,
            self.mock_diversification,
            mock_debate
        )

        self.assertEqual(result["decision"], "BUY")

    def test_sell_signal(self):
        mock_debate = {
            "bullish_arguments": [],
            "bearish_arguments": ["Bad earnings"],
            "conflicts": []
        }

        result = self.agent.decide(
            self.mock_fundamental,
            self.mock_technical_sell,
            self.mock_risk_high,
            self.mock_sentiment_negative,
            self.mock_diversification,
            mock_debate
        )

        self.assertEqual(result["decision"], "SELL")

    def test_hold_on_conflict(self):
        mock_debate = {
            "bullish_arguments": ["Good news"],
            "bearish_arguments": ["Bad news"],
            "conflicts": ["Mixed signals", "Volatility"]
        }

        result = self.agent.decide(
            self.mock_fundamental,
            self.mock_technical_hold,
            self.mock_risk_low,
            self.mock_sentiment_positive,
            self.mock_diversification,
            mock_debate
        )

        self.assertEqual(result["decision"], "HOLD")


if __name__ == "__main__":
    unittest.main()
