import json

from agents.decision_agent import LABEL_ACTIONS
from agents.llm.client import LlmError
from agents.llm.prompts import DEBATE_SYSTEM
from agents.llm.signals import context_signals

STANCES = {"bullish": 1, "positive": 1, "bearish": -1, "negative": -1, "high": -1}
DEBATE_FIELDS = ("bull_case", "bear_case", "verdict")


class DebateAgent:
    """Moderates conflicting agent signals and settles the final action."""

    name = "debate"

    def __init__(self, client):
        self.client = client

    def has_conflict(self, board):
        stances = {STANCES.get(output["signal"], 0) for output in context_signals(board).values()}
        return 1 in stances and -1 in stances

    def moderate(self, board):
        rule_decision = board["decision"]
        if not self.has_conflict(board):
            return {**rule_decision, "source": "rules", "debate": None, "note": None}

        prompt = (
            f"Agent outputs:\n{json.dumps(context_signals(board), indent=2)}\n\n"
            f"Rule-based decision: {rule_decision['label']}"
        )

        try:
            debate = self.client.complete_json(DEBATE_SYSTEM, prompt)
            label = str(debate.get("action", "")).strip().upper()
            if label not in LABEL_ACTIONS:
                raise LlmError(f"Moderator returned an invalid action: {label!r}")
        except LlmError as exc:
            return {**rule_decision, "source": "rules", "debate": None, "note": f"Debate unavailable: {exc}"}

        return {
            "action": LABEL_ACTIONS[label],
            "label": label,
            "source": "debate",
            "debate": {field: str(debate.get(field, "")) for field in DEBATE_FIELDS},
            "note": None,
        }
