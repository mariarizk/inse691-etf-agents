import unittest
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from agents.efficiency_agent import EfficiencyAgent

class TestEfficiencyAgent(unittest.TestCase):

    def setUp(self):
        self.thresholds = {
            "roe": {"good": 0.15, "neutral": 0.08},
            "roa": {"good": 0.08, "neutral": 0.04},
            "asset_turnover": {"good": 0.7, "neutral": 0.3}
        }
        self.agent = EfficiencyAgent(self.thresholds)

    def test_analyze_company(self):
        result = self.agent.analyze_company("AAPL")

        self.assertNotIn("error", result)

        required_keys = [
            "roa", "roe", "asset_turnover",
            "roa_score", "roe_score", "asset_turnover_score",
            "efficiency_score"
        ]

        for key in required_keys:
            self.assertIn(key, result, f"Missing key: {key}")
            self.assertIsNotNone(result[key], f"{key} is None")

        self.assertIsInstance(result["efficiency_score"], float)

if __name__ == "__main__":
    unittest.main()
