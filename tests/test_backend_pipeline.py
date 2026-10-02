import sys
import os
import unittest

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.etf_pipeline import ETFPipeline
from config import CONFIG


class TestETFMultiAgentPipeline(unittest.TestCase):

    def setUp(self):
        # FIX: your pipeline requires a config argument
        self.pipeline = ETFPipeline(CONFIG)

    def test_pipeline_run(self):
        """Test full MAS pipeline output structure."""
        result = self.pipeline.run("AAPL")

        # === Top-level keys ===
        self.assertIn("agents", result, "Missing 'agents' section")
        self.assertIn("debate", result, "Missing 'debate' section")
        self.assertIn("decision", result, "Missing 'decision' section")
        self.assertIn("status", result, "Missing 'status' section")

        # === Agent-level keys ===
        required_agents = [
            "fundamental",
            "technical",
            "risk",
            "sentiment",
            "diversification"
        ]

        for key in required_agents:
            self.assertIn(
                key,
                result["agents"],
                f"Missing agent output: {key}"
            )

        # === Debate Agent Output ===
        debate = result["debate"]
        self.assertIn("bullish_arguments", debate)
        self.assertIn("bearish_arguments", debate)
        self.assertIn("conflicts", debate)

        # === Decision Agent Output ===
        decision = result["decision"]
        self.assertIn("decision", decision)
        self.assertIn("confidence", decision)

        # === Coordinator Status ===
        status = result["status"]
        self.assertIn("complete", status)
        self.assertIn("missing", status)

        # === Print for debugging ===
        print("\n=== Pipeline Output ===")
        print("Agents:", result["agents"].keys())
        print("Decision:", decision)
        print("Status:", status)


if __name__ == "__main__":
    unittest.main()
