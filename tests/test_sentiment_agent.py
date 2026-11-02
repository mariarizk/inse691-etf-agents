import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from agents.llm_client import LlmError
from agents.sentiment_agent import SentimentAgent

ARTICLE = """
NVIDIA shares fell after regulators announced a new review
of AI chip exports. Analysts expect the restrictions to
reduce future revenue growth.
"""


def prices(values):
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


class TestSentimentAgent(unittest.TestCase):

    def test_classifies_news_with_llm(self):
        llm = FakeLlm({"sentiment": "negative", "confidence": 88, "reasoning": "Export review hurts revenue."})
        result = SentimentAgent(llm).analyze(prices([100, 101]), ARTICLE)

        self.assertEqual(result["sentiment"], "Negative")
        self.assertEqual(result["confidence"], 88)
        self.assertEqual(result["source"], "llm")
        self.assertIn("AI chip exports", llm.prompts[0])

    def test_uses_price_momentum_without_news(self):
        result = SentimentAgent(FakeLlm()).analyze(prices([100, 102]))

        self.assertEqual(result["sentiment"], "Positive")
        self.assertEqual(result["source"], "price")
        self.assertEqual(result["confidence"], 100)

    def test_small_move_without_news_is_neutral(self):
        self.assertEqual(SentimentAgent().analyze(prices([100, 100.5]))["sentiment"], "Neutral")

    def test_falls_back_to_price_when_llm_fails(self):
        result = SentimentAgent(FakeLlm(error=LlmError("quota exceeded"))).analyze(prices([100, 98]), ARTICLE)

        self.assertEqual(result["sentiment"], "Negative")
        self.assertEqual(result["source"], "price")
        self.assertIn("quota exceeded", result["reasoning"])

    def test_rejects_unknown_label(self):
        llm = FakeLlm({"sentiment": "Bullish", "confidence": 90, "reasoning": "..."})
        self.assertEqual(SentimentAgent(llm).analyze(prices([100, 100]), ARTICLE)["source"], "price")


if __name__ == "__main__":
    unittest.main()
