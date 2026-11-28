import os
import sys
import unittest
from unittest.mock import patch

import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from backend.etf_pipeline import ETFPipeline


class TestETFPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = ETFPipeline()
        self.price_df = pd.read_csv(
            "data/QQQ.csv",
            parse_dates=["Date"],
            index_col="Date",
        )
        self.article = (
            "Microsoft reported stronger-than-expected earnings "
            "and raised guidance for next quarter. Analysts "
            "remain optimistic regarding future growth."
        )

    def test_pipeline_run_offline_rule_based(self):
        result = self.pipeline.run(self.price_df, self.article)

        self.assertIn("technical", result)
        self.assertIn("sentiment", result)
        self.assertIn("risk", result)
        self.assertIn("decision", result)
        self.assertIn("explanation", result)
        self.assertIn(
            result["technical"],
            ["bullish", "bearish", "neutral"],
        )
        self.assertIn(result["decision"]["action"], [-1, 0, 1])
        self.assertIn("pipeline_result", self.pipeline.blackboard.all())

    def test_sentiment_structure(self):
        result = self.pipeline.run(self.price_df, self.article)
        sentiment = result["sentiment"]
        self.assertIn(
            sentiment["sentiment"],
            ["Positive", "Neutral", "Negative"],
        )
        self.assertTrue(0 <= sentiment["confidence"] <= 100)

    def test_risk_structure(self):
        result = self.pipeline.run(self.price_df, self.article)
        risk = result["risk"]
        self.assertIn(risk["risk"], ["Low", "Medium", "High"])
        self.assertTrue(0 <= risk["confidence"] <= 100)

    def test_decision_structure(self):
        result = self.pipeline.run(self.price_df, self.article)
        self.assertIn(result["decision"]["action"], [-1, 0, 1])

    def test_pipeline_fallback_on_sentiment_failure(self):
        with patch.object(
            self.pipeline.sentiment_agent,
            "analyze",
            side_effect=RuntimeError("forced failure"),
        ):
            result = self.pipeline.run(self.price_df, self.article)

        self.assertEqual(result["sentiment"]["tool_used"], "pipeline_fallback")
        self.assertEqual(result["sentiment"]["sentiment"], "Neutral")


if __name__ == "__main__":
    unittest.main()
