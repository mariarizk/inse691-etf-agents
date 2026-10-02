import unittest
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from agents.cash_flow_agent import CashFlowAgent

class TestCashFlowAgent(unittest.TestCase):

    def setUp(self):
        self.thresholds = {
            "cash_flow_margin": {"good": 0.20, "neutral": 0.10},
            "fcf_margin": {"good": 0.10, "neutral": 0.00},
            "ocf_growth": {"good": 0.10, "neutral": 0.00}
        }
        self.agent = CashFlowAgent(self.thresholds)

    def test_analyze_company(self):
        result = self.agent.analyze_company("AAPL")

        # Ensure no error
        self.assertNotIn("error", result)

        required_keys = [
            "cash_flow_margin",
            "fcf_margin",
            "ocf_growth",
            "fcf_growth",
            "cash_strength_score",
            "fcf_score",
            "growth_score",
            "cashflow_score"
        ]

        for key in required_keys:
            self.assertIn(key, result, f"Missing key: {key}")
            self.assertIsNotNone(result[key], f"{key} is None")

        # Final score must be float
        self.assertIsInstance(result["cashflow_score"], float)

if __name__ == "__main__":
    unittest.main()
