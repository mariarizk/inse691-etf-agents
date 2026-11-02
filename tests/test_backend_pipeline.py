import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from agents.decision_agent import ACTION_LABELS
from backend.etf_pipeline import ETFPipeline


class FakeLlm:
    """Answers both news agents with a bullish, low-risk reading and returns scripted explanations."""

    def __init__(self, explanations):
        self.explanations = list(explanations)

    def complete_json(self, system_prompt, user_prompt):
        return {"sentiment": "Positive", "risk": "Low", "confidence": 90, "reasoning": "Strong earnings."}

    def complete(self, system_prompt, user_prompt):
        return self.explanations.pop(0)


class TestETFPipeline(unittest.TestCase):

    def setUp(self):
        values = [100 + i for i in range(40)]
        self.price_df = pd.DataFrame(
            {"Close": values}, index=pd.date_range("2025-01-01", periods=len(values))
        )

    def test_blackboard_holds_every_agent_output(self):
        result = ETFPipeline().run(self.price_df)

        for agent in ("technical", "sentiment", "risk", "decision"):
            self.assertIn(agent, result)
        self.assertNotIn("explanation", result)
        self.assertEqual(result["sentiment"]["source"], "price")

    def test_blackboard_logs_every_message_in_order(self):
        result = ETFPipeline().run(self.price_df)
        log = result["log"]

        self.assertEqual([entry["sender"] for entry in log], ["technical", "sentiment", "risk", "decision"])
        self.assertEqual([entry["step"] for entry in log], [1, 2, 3, 4])
        self.assertEqual(log[-1]["content"], result["decision"])

    def test_decision_is_a_valid_action(self):
        decision = ETFPipeline().run(self.price_df)["decision"]

        self.assertIn(decision["action"], ACTION_LABELS)
        self.assertEqual(decision["label"], ACTION_LABELS[decision["action"]])

    def test_llm_run_explains_the_decision(self):
        llm = FakeLlm(["The system recommends BUY: the trend is bullish, sentiment is positive and risk is low."])
        result = ETFPipeline(llm).run(self.price_df, "Strong earnings beat.", explain=True)

        self.assertEqual(result["decision"]["label"], "BUY")
        self.assertEqual(result["sentiment"]["source"], "llm")
        self.assertTrue(result["explanation"]["consistent"])
        self.assertEqual(result["log"][-1]["sender"], "explanation")

    def test_inconsistent_explanation_is_regenerated_once(self):
        llm = FakeLlm([
            "The system recommends SELL because the trend is bearish.",
            "The system recommends BUY: the trend is bullish, sentiment is positive and risk is low.",
        ])
        explanation = ETFPipeline(llm).run(self.price_df, "Strong earnings beat.", explain=True)["explanation"]

        self.assertTrue(explanation["consistent"])
        self.assertEqual(explanation["attempts"], 2)


if __name__ == "__main__":
    unittest.main()
