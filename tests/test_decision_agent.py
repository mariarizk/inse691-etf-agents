import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.blackboard import Blackboard
from agents.decision_agent import DecisionAgent


class TestDecisionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = DecisionAgent()

    def test_buy_when_all_agents_agree(self):
        self.assertEqual(self.agent.decide("bullish", "positive", "low"), 1)

    def test_sell_on_any_bearish_signal(self):
        self.assertEqual(self.agent.decide("bearish", "positive", "low"), -1)
        self.assertEqual(self.agent.decide("bullish", "negative", "low"), -1)
        self.assertEqual(self.agent.decide("bullish", "positive", "high"), -1)

    def test_hold_on_mixed_signals(self):
        self.assertEqual(self.agent.decide("neutral", "positive", "low"), 0)
        self.assertEqual(self.agent.decide("bullish", "positive", "medium"), 0)
        self.assertEqual(self.agent.decide("bullish", "neutral", "low"), 0)

    def test_reads_signals_from_blackboard(self):
        board = Blackboard()
        board.write("technical", {"signal": "bullish"})
        board.write("sentiment", {"signal": "positive"})
        board.write("risk", {"signal": "low"})

        self.assertEqual(self.agent.decide_from_blackboard(board), {"action": 1, "label": "BUY"})


if __name__ == "__main__":
    unittest.main()
