import unittest
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from agents.balance_sheet_agent import BalanceSheetAgent

class TestBalanceSheetAgent(unittest.TestCase):

    def setUp(self):
        self.thresholds = {
            "current_ratio": {"good": 1.5, "neutral": 1.0},
            "debt_to_equity": {"good": 1.0, "neutral": 2.0},
            "cash_ratio": {"good": 0.5, "neutral": 0.2}
        }
        self.agent = BalanceSheetAgent(self.thresholds)

    def test_analyze_company(self):
        result = self.agent.analyze_company("AAPL")

        # Ensure no error
        self.assertNotIn("error", result)

        # Required keys
        required_keys = [
            "current_ratio", "quick_ratio", "debt_to_equity",
            "debt_ratio", "cash_ratio",
            "liquidity_score", "debt_score", "cash_score",
            "balance_sheet_score"
        ]

        for key in required_keys:
            self.assertIn(key, result, f"Missing key: {key}")
            self.assertIsNotNone(result[key], f"{key} is None")

        # Types
        self.assertIsInstance(result["current_ratio"], float)
        self.assertIsInstance(result["quick_ratio"], float)
        self.assertIsInstance(result["debt_to_equity"], float)
        self.assertIsInstance(result["debt_ratio"], float)
        self.assertIsInstance(result["cash_ratio"], float)

        self.assertIsInstance(result["liquidity_score"], int)
        self.assertIsInstance(result["debt_score"], int)
        self.assertIsInstance(result["cash_score"], int)

        self.assertIsInstance(result["balance_sheet_score"], float)

        # Score range
        self.assertGreaterEqual(result["balance_sheet_score"], 1)
        self.assertLessEqual(result["balance_sheet_score"], 3)

if __name__ == "__main__":
    unittest.main()
