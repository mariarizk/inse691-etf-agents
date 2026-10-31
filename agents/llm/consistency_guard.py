import re

from agents.llm.signals import context_signals

ACTION_WORDS = {"BUY": r"buy(?:ing)?", "HOLD": r"hold(?:ing)?", "SELL": r"sell(?:ing)?"}
RECOMMENDATION = re.compile(
    r"\b(?:recommend\w*|final (?:decision|action)|decision is|action is)\W+(?:\w+\W+){0,3}?(buy|hold|sell)(?:ing)?\b"
)
AGENT_TERMS = {
    "technical": r"technical|trend|moving averages?",
    "sentiment": r"(?<!news )sentiment|daily return|momentum",
    "risk": r"risk|volatility",
    "news_sentiment": r"news|headlines?",
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


def check(explanation, final_decision, board):
    """Rule-based hallucination guard: the explanation must agree with the actual decision and signals."""
    text = explanation.lower()
    final = final_decision["label"]
    issues = []

    if not re.search(rf"\b{ACTION_WORDS[final]}\b", text):
        issues.append(f"It does not state the final action {final}.")

    for match in RECOMMENDATION.finditer(text):
        recommended = match.group(1).upper()
        if recommended != final:
            issues.append(f"It recommends {recommended}, but the final action is {final}.")

    for agent, output in context_signals(board).items():
        opposite = OPPOSITES.get(output["signal"])
        if opposite and re.search(rf"\b(?:{AGENT_TERMS[agent]}){NEARBY_WORDS}{opposite}\b", text):
            issues.append(f"It describes the {agent} agent as {opposite}, but its signal is {output['signal']}.")

    return {"consistent": not issues, "issues": issues}
