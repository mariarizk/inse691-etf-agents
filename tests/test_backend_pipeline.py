import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from agents.decision_agent import ACTION_LABELS
from backend.etf_pipeline import ETFPipeline


class TestETFPipeline(unittest.TestCase):

    def setUp(self):
        values = [100 + i for i in range(40)]
        self.price_df = pd.DataFrame(
            {"Close": values}, index=pd.date_range("2025-01-01", periods=len(values))
        )

    def test_blackboard_holds_every_agent_output(self):
        result = ETFPipeline(self.price_df).run()

        for agent in ("technical", "sentiment", "risk", "decision"):
            self.assertIn(agent, result)

        for agent in ("technical", "sentiment", "risk"):
            self.assertIn("signal", result[agent])

    def test_blackboard_logs_every_message_in_order(self):
        pipeline = ETFPipeline(self.price_df)
        result = pipeline.run()
        log = pipeline.blackboard.history()

        self.assertEqual([entry["sender"] for entry in log], ["technical", "sentiment", "risk", "decision"])
        self.assertEqual([entry["step"] for entry in log], [1, 2, 3, 4])
        self.assertEqual(log[-1]["content"], result["decision"])
        for entry in log:
            self.assertIn("timestamp", entry)

    def test_decision_is_a_valid_action(self):
        decision = ETFPipeline(self.price_df).run()["decision"]

        self.assertIn(decision["action"], ACTION_LABELS)
        self.assertEqual(decision["label"], ACTION_LABELS[decision["action"]])


if __name__ == "__main__":
    unittest.main()
