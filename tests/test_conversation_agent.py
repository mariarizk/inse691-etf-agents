import os
import sys
import unittest
from unittest.mock import patch

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from agents.conversation_agent import ConversationAgent


class TestConversationAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ConversationAgent()
        self.analysis = {
            "technical": "bullish",
            "sentiment": {
                "sentiment": "Positive",
                "confidence": 80,
                "reasoning": "Growth outlook.",
            },
            "risk": {
                "risk": "Low",
                "confidence": 75,
                "reasoning": "Stable conditions.",
            },
            "decision": {
                "action": 1,
                "action_label": "BUY",
                "reasoning": "Aligned signals.",
            },
            "explanation": {
                "explanation": "Buy because signals align.",
                "consistency": True,
            },
        }
        self.agent.store_analysis(
            "Microsoft beat earnings and raised guidance for cloud growth.",
            self.analysis,
        )

    def test_store_analysis_memory(self):
        self.assertIsNotNone(self.agent.session_state["last_article"])
        self.assertEqual(
            self.agent.session_state["last_analysis"]["decision"]["action_label"],
            "BUY",
        )

    def test_retrieve_decision_tool(self):
        retrieved = self.agent._execute_tool("retrieve_decision")
        self.assertEqual(retrieved["action_label"], "BUY")

    def test_chat_with_mocked_llm(self):
        with patch.object(
            self.agent,
            "_select_tool",
            return_value="retrieve_decision",
        ), patch.object(
            self.agent.gemini,
            "generate",
            return_value="The recommendation is BUY based on aligned signals.",
        ):
            response = self.agent.chat("What was the final decision?")

        self.assertIn("BUY", response)
        self.assertEqual(len(self.agent.session_state["chat_history"]), 1)


if __name__ == "__main__":
    unittest.main()
