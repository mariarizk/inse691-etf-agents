import unittest
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from agents.income_statement_agent import IncomeStatementAgent

class TestIncomeStatementAgent(unittest.TestCase):

    def setUp(self):
        self.thresholds = {
            "net_margin": {"good": 0.15, "neutral": 0.05},
            "revenue_growth": {"good": 0.10, "neutral": 0.00},
            "eps": {"good": 0.0, "neutral": -0.1}
        }
        self.agent = IncomeStatementAgent(self.thresholds)

    def test_analyze_company(self):
        result = self.agent.analyze_company("AAPL")

        self.assertNotIn("error", result)

        required_keys = [
            "gross_margin", "operating_margin", "net_margin",
            "revenue_growth", "net_income_growth", "eps",
            "profitability_score", "growth_score", "eps_score",
            "income_statement_score"
        ]

        for key in required_keys:
            self.assertIn(key, result)
            self.assertIsNotNone(result[key])

        self.assertIsInstance(result["income_statement_score"], float)

if __name__ == "__main__":
    unittest.main()
