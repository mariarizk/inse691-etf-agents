ANALYST_AGENTS = ("technical", "sentiment", "risk")
ACTION_LABELS = {1: "BUY", 0: "HOLD", -1: "SELL"}
LABEL_ACTIONS = {label: action for action, label in ACTION_LABELS.items()}


class DecisionAgent:
    name = "decision"

    def decide(self, tech, sentiment, risk):

        if tech == "bearish" or sentiment == "negative" or risk == "high":
            return -1   # SELL

        if tech == "neutral" or risk == "medium":
            return 0    # HOLD

        if tech == "bullish" and sentiment == "positive" and risk == "low":
            return 1    # BUY

        return 0

    def decide_from_blackboard(self, blackboard):
        action = self.decide(
            blackboard.read("technical")["signal"],
            blackboard.read("sentiment")["signal"],
            blackboard.read("risk")["signal"],
        )
        return {"action": action, "label": ACTION_LABELS[action]}
