from config import AGENT_CONFIG

ANALYST_AGENTS = ("technical", "sentiment", "risk")
ACTION_LABELS = {1: "BUY", 0: "HOLD", -1: "SELL"}


class DecisionAgent:

    name = "decision"

    def __init__(self, settings=None):
        self.min_confidence = (settings or AGENT_CONFIG["decision"])["min_confidence"]

    def decide(self, technical, sentiment, risk):

        sentiment_label = sentiment["sentiment"]
        sentiment_confidence = sentiment["confidence"]

        risk_label = risk["risk"]
        risk_confidence = risk["confidence"]

        # Ignore weak LLM outputs
        if sentiment_confidence < self.min_confidence:
            sentiment_label = "Neutral"

        if risk_confidence < self.min_confidence:
            risk_label = "Medium"

        signals = f"Technical={technical}, Sentiment={sentiment_label}, Risk={risk_label}"

        # SELL
        if (
            technical == "bearish"
            or sentiment_label == "Negative"
            or risk_label == "High"
        ):
            return self._result(-1, signals)

        # BUY
        if (
            technical == "bullish"
            and sentiment_label == "Positive"
            and risk_label == "Low"
        ):
            return self._result(1, signals)

        # HOLD
        return self._result(0, f"Mixed signals: {signals}")

    def decide_from_blackboard(self, blackboard):
        return self.decide(
            blackboard.read("technical")["signal"],
            blackboard.read("sentiment"),
            blackboard.read("risk"),
        )

    def _result(self, action, reasoning):
        return {"action": action, "label": ACTION_LABELS[action], "reasoning": reasoning}
