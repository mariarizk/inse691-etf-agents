import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import unittest

from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent


class TestGuardrails(unittest.TestCase):

    def setUp(self):

        self.sentiment = SentimentAgent()
        self.risk = RiskAgent()

    def test_empty_article_sentiment(self):

        with self.assertRaises(ValueError):
            self.sentiment.analyze("")

    def test_empty_article_risk(self):

        with self.assertRaises(ValueError):
            self.risk.analyze("")

    def test_short_article_sentiment(self):

        with self.assertRaises(ValueError):
            self.sentiment.analyze("QQQ")

    def test_short_article_risk(self):

        with self.assertRaises(ValueError):
            self.risk.analyze("QQQ")


if __name__ == "__main__":
    unittest.main()
