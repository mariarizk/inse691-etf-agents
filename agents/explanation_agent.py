import json
import re

from agents.decision_agent import ANALYST_AGENTS
from agents.llm_client import LlmError
from config import LLM_CONFIG

SYSTEM_PROMPT = """You explain trading decisions made by a multi-agent system for the QQQ ETF
to a non-expert investor.

Justify the final action using the agent outputs provided, and say which agents supported or
opposed it. State the final action explicitly as BUY, HOLD or SELL and describe each agent's
signal exactly as given. Write one short paragraph of at most {max_words} words. Do not invent
data and do not give personalised financial advice."""

RETRY_PROMPT = """Your previous explanation was:
{previous}

It failed these consistency checks:
{issues}

Rewrite the explanation so that it passes every check."""

ACTION_WORDS = {"BUY": r"buy(?:ing)?", "HOLD": r"hold(?:ing)?", "SELL": r"sell(?:ing)?"}
RECOMMENDATION = re.compile(
    r"\b(?:recommend\w*|final (?:decision|action)|decision is|action is)\W+(?:\w+\W+){0,3}?(buy|hold|sell)(?:ing)?\b"
)
SIGNAL_FIELDS = {"technical": "signal", "sentiment": "sentiment", "risk": "risk"}
AGENT_TERMS = {
    "technical": r"technical|trend|moving averages?",
    "sentiment": r"sentiment|news tone|momentum",
    "risk": r"risk|volatility",
}
OPPOSITES = {
    "bullish": "bearish",
    "bearish": "bullish",
    "positive": "negative",
    "negative": "positive",
    "low": "high",
    "high": "low",
}
NEARBY_WORDS = r"\W+(?:\w+\W+){0,3}?"


def check_consistency(explanation, board):
    """Rule-based hallucination check: the explanation must agree with the decision and agent signals."""
    text = explanation.lower()
    final = board["decision"]["label"]
    issues = []

    if not re.search(rf"\b{ACTION_WORDS[final]}\b", text):
        issues.append(f"It does not state the final action {final}.")

    for match in RECOMMENDATION.finditer(text):
        recommended = match.group(1).upper()
        if recommended != final:
            issues.append(f"It recommends {recommended}, but the final action is {final}.")

    for agent, field in SIGNAL_FIELDS.items():
        signal = str(board[agent][field]).lower()
        opposite = OPPOSITES.get(signal)
        if opposite and re.search(rf"\b(?:{AGENT_TERMS[agent]}){NEARBY_WORDS}{opposite}\b", text):
            issues.append(f"It describes the {agent} agent as {opposite}, but its signal is {signal}.")

    return {"consistent": not issues, "issues": issues}


class ExplanationAgent:
    """Justifies the final BUY / HOLD / SELL decision in plain language."""

    name = "explanation"

    def __init__(
        self,
        llm_client,
        max_words=LLM_CONFIG["explanation_max_words"],
        max_attempts=LLM_CONFIG["explanation_max_attempts"],
    ):
        self.llm = llm_client
        self.system_prompt = SYSTEM_PROMPT.format(max_words=max_words)
        self.max_attempts = max_attempts

    def explain(self, board):
        payload = json.dumps({name: board[name] for name in ANALYST_AGENTS + ("decision",)}, indent=2, default=str)

        result = {"text": "", "consistent": None, "issues": [], "attempts": 0}
        prompt = payload

        for attempt in range(1, self.max_attempts + 1):
            try:
                text = self.llm.complete(self.system_prompt, prompt)
            except LlmError as exc:
                if result["text"]:
                    return result
                return {**result, "text": f"Explanation unavailable: {exc}"}

            result = {"text": text, **check_consistency(text, board), "attempts": attempt}
            if result["consistent"]:
                break

            retry = RETRY_PROMPT.format(previous=text, issues="\n".join(f"- {i}" for i in result["issues"]))
            prompt = f"{payload}\n\n{retry}"

        return result
