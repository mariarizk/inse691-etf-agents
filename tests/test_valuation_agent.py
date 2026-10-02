import unittest
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from agents.valuation_agent import ValuationAgent

class TestValuationAgent(unittest.TestCase):

    def setUp(self):
        self.thresholds = {
            "pe": {"good": 15, "neutral": 25},
            "peg": {"good": 1.0, "neutral": 1.5},
            "ps": {"good": 3.0, "neutral": 6.0},
            "pb": {"good": 3.0, "neutral": 6.0},
            "ev_ebitda": {"good": 10, "neutral": 15}
        }
        self.agent = ValuationAgent(self.thresholds)

    def test_analyze_company(self):
        result = self.agent.analyze_company("AAPL")

        self.assertNotIn("error", result)

        required_keys = [
            "pe", "forward_pe", "peg", "ps", "pb", "ev_ebitda",
            "pe_score", "peg_score", "ps_score", "pb_score", "ev_ebitda_score",
            "valuation_score"
        ]

        for key in required_keys:
            self.assertIn(key, result, f"Missing key: {key}")
            self.assertIsNotNone(result[key], f"{key} is None")

        self.assertIsInstance(result["valuation_score"], float)

if __name__ == "__main__":
    unittest.main()
