import json

from agents.decision_agent import ANALYST_AGENTS
from agents.llm.client import LlmError
from agents.llm.prompts import EXPLANATION_SYSTEM
from config import LLM_CONFIG


class ExplanationAgent:
    """Justifies the final BUY / HOLD / SELL action in plain language."""

    name = "explanation"

    def __init__(self, client, max_words=LLM_CONFIG["explanation_max_words"]):
        self.client = client
        self.system_prompt = EXPLANATION_SYSTEM.format(max_words=max_words)

    def explain(self, board, final_decision):
        debate = final_decision["debate"] or {}
        payload = {
            "signals": {name: board[name] for name in ANALYST_AGENTS},
            "rule_based_decision": board["decision"]["label"],
            "final_decision": final_decision["label"],
            "decided_by": final_decision["source"],
            "debate_verdict": debate.get("verdict"),
        }

        try:
            return self.client.complete(self.system_prompt, json.dumps(payload, indent=2))
        except LlmError as exc:
            return f"Explanation unavailable: {exc}"
