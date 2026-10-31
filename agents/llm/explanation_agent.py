import json

from agents.llm import consistency_guard
from agents.llm.client import LlmError
from agents.llm.prompts import EXPLANATION_RETRY, EXPLANATION_SYSTEM
from agents.llm.signals import context_signals
from config import LLM_CONFIG


class ExplanationAgent:
    """Justifies the final BUY / HOLD / SELL action and checks the text against the real signals."""

    name = "explanation"

    def __init__(
        self,
        client,
        max_words=LLM_CONFIG["explanation_max_words"],
        max_attempts=LLM_CONFIG["explanation_max_attempts"],
    ):
        self.client = client
        self.system_prompt = EXPLANATION_SYSTEM.format(max_words=max_words)
        self.max_attempts = max_attempts

    def explain(self, board, final_decision):
        debate = final_decision["debate"] or {}
        payload = json.dumps({
            "signals": context_signals(board),
            "rule_based_decision": board["decision"]["label"],
            "final_decision": final_decision["label"],
            "decided_by": final_decision["source"],
            "debate_verdict": debate.get("verdict"),
        }, indent=2)

        result = {"text": "", "consistent": None, "issues": [], "attempts": 0}
        prompt = payload

        for attempt in range(1, self.max_attempts + 1):
            try:
                text = self.client.complete(self.system_prompt, prompt)
            except LlmError as exc:
                if result["text"]:
                    return result
                return {**result, "text": f"Explanation unavailable: {exc}"}

            result = {"text": text, **consistency_guard.check(text, final_decision, board), "attempts": attempt}
            if result["consistent"]:
                break

            retry = EXPLANATION_RETRY.format(previous=text, issues="\n".join(f"- {i}" for i in result["issues"]))
            prompt = f"{payload}\n\n{retry}"

        return result
