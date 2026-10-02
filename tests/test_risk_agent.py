import unittest
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from agents.risk_agent import RiskAgent

class TestRiskAgent(unittest.TestCase):

    def setUp(self):
        self.risk_thresholds = {
            "beta": {"good": 1.0, "neutral": 1.2},
            "volatility": {"good": 0.02, "neutral": 0.04},
            "drawdown": {"good": 0.10, "neutral": 0.20},
            "debt_to_equity": {"good": 1.0, "neutral": 2.0},
            "current_ratio": {"good": 1.5, "neutral": 1.0}
        }

        self.bs_thresholds = {
            "current_ratio": {"good": 1.5, "neutral": 1.0},
            "debt_to_equity": {"good": 1.0, "neutral": 2.0},
            "cash_ratio": {"good": 0.5, "neutral": 0.2}
        }

        self.agent = RiskAgent(self.risk_thresholds, self.bs_thresholds)

    def test_analyze_company(self):
        result = self.agent.analyze_company("AAPL")

        self.assertNotIn("error", result)

        required_keys = [
            "beta", "volatility", "max_drawdown",
            "debt_to_equity", "current_ratio",
            "beta_score", "volatility_score", "drawdown_score",
            "debt_score", "liquidity_score",
            "risk_score"
        ]

        for key in required_keys:
            self.assertIn(key, result)
            self.assertIsNotNone(result[key])

        self.assertIsInstance(result["risk_score"], float)

if __name__ == "__main__":
    unittest.main()
