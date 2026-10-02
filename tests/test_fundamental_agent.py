import unittest
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from agents.fundamental_agent import FundamentalAgent


class TestFundamentalAgent(unittest.TestCase):

    def setUp(self):
        self.bs_thresholds = {
            "current_ratio": {"good": 1.5, "neutral": 1.0},
            "debt_to_equity": {"good": 1.0, "neutral": 2.0},
            "cash_ratio": {"good": 0.5, "neutral": 0.2},
        }
        self.is_thresholds = {
            "net_margin": {"good": 0.15, "neutral": 0.05},
            "revenue_growth": {"good": 0.10, "neutral": 0.00},
            "eps": {"good": 0.0, "neutral": -0.1},
        }
        self.cf_thresholds = {
            "cash_flow_margin": {"good": 0.20, "neutral": 0.10},
            "fcf_margin": {"good": 0.10, "neutral": 0.00},
            "ocf_growth": {"good": 0.10, "neutral": 0.00},
        }
        self.val_thresholds = {
            "pe": {"good": 15, "neutral": 25},
            "peg": {"good": 1.0, "neutral": 1.5},
            "ps": {"good": 3.0, "neutral": 6.0},
            "pb": {"good": 3.0, "neutral": 6.0},
            "ev_ebitda": {"good": 10, "neutral": 15},
        }
        self.eff_thresholds = {
            "roe": {"good": 0.15, "neutral": 0.08},
            "roa": {"good": 0.08, "neutral": 0.04},
            "asset_turnover": {"good": 0.7, "neutral": 0.3},
        }

        self.agent = FundamentalAgent(
            self.bs_thresholds,
            self.is_thresholds,
            self.cf_thresholds,
            self.val_thresholds,
            self.eff_thresholds,
        )

    def test_analyze_company(self):
        result = self.agent.analyze_company("AAPL")

        self.assertNotIn("error", result)

        required_keys = [
            "balance_sheet_score",
            "income_statement_score",
            "cashflow_score",
            "valuation_score",
            "efficiency_score",
            "fundamental_score",
        ]

        for key in required_keys:
            self.assertIn(key, result, f"Missing key: {key}")
            self.assertIsNotNone(result[key], f"{key} is None")

        self.assertIsInstance(result["fundamental_score"], float)


if __name__ == "__main__":
    unittest.main()
