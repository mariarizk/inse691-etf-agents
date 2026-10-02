class DecisionAgent:
    def decide(self, tech, sentiment, risk):

        if tech == "bearish" or sentiment == "negative" or risk == "high":
            return -1   # SELL

        if tech == "neutral" or risk == "medium":
            return 0    # HOLD

        if tech == "bullish" and sentiment == "positive" and risk == "low":
            return 1    # BUY

        return 0
