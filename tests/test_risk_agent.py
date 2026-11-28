import os
import sys
import unittest

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from agents.risk_agent import RiskAgent


class TestRiskAgent(unittest.TestCase):

    def setUp(self):
        self.agent = RiskAgent()
        self.article = (
            "NVIDIA is facing increased regulatory scrutiny regarding "
            "AI chip exports. Analysts believe additional restrictions "
            "could impact future revenue growth amid litigation risk."
        )

    def test_analyze_returns_valid_structure(self):
        result = self.agent.analyze(self.article)
        self.assertIn(result["risk"], ["Low", "Medium", "High"])
        self.assertTrue(0 <= result["confidence"] <= 100)
        self.assertGreater(len(result["reasoning"]), 0)
        self.assertIn("tool_used", result)

    def test_rule_based_high_risk_keywords(self):
        result = self.agent._rule_based_analysis(
            "The company faces a lawsuit and regulatory action."
        )
        self.assertEqual(result["risk"], "High")


if __name__ == "__main__":
    unittest.main()
