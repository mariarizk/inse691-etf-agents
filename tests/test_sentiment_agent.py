import os
import sys
import unittest

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from agents.sentiment_agent import SentimentAgent


class TestSentimentAgent(unittest.TestCase):

    def setUp(self):
        self.agent = SentimentAgent()
        self.article = (
            "Microsoft reported stronger-than-expected earnings and "
            "raised guidance for next quarter. Analysts expect growth "
            "to continue through the year with strong profits."
        )

    def test_analyze_returns_valid_structure(self):
        result = self.agent.analyze(self.article)
        self.assertIn(result["sentiment"], ["Positive", "Neutral", "Negative"])
        self.assertTrue(0 <= result["confidence"] <= 100)
        self.assertGreater(len(result["reasoning"]), 0)
        self.assertIn("tool_used", result)

    def test_rule_based_positive_keywords(self):
        result = self.agent._rule_based_analysis(self.article)
        self.assertEqual(result["sentiment"], "Positive")
        self.assertEqual(
            result["tool_used"],
            "rule_based_sentiment_analysis",
        )


if __name__ == "__main__":
    unittest.main()
