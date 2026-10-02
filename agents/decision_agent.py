class DecisionAgent:
    def __init__(self):
        pass

    def decide(self, fundamental, technical, risk, sentiment, diversification, debate):
        bullish = len(debate["bullish_arguments"])
        bearish = len(debate["bearish_arguments"])
        conflicts = len(debate["conflicts"])

        technical_signal = technical["signal"]
        fundamental_score = fundamental["score"]
        risk_score = risk["risk_score"]
        sentiment_score = sentiment["sentiment_score"]
        diversification_score = diversification["score"]
        div_score = diversification.get("final_diversification_score", 0)

        # -----------------------------
        # 0. Technical overrides (ALWAYS FIRST)
        # -----------------------------
        if technical_signal == "BUY":
            return {"decision": "BUY", "confidence": 70}

        if technical_signal == "SELL":
            return {"decision": "SELL", "confidence": 70}

        # -----------------------------
        # 1. Strong BUY override
        # -----------------------------
        if bullish > bearish:
            return {"decision": "BUY", "confidence": 60}

        # -----------------------------
        # 2. Strong SELL override
        # -----------------------------
        if bearish > bullish:
            return {"decision": "SELL", "confidence": 60}

        # -----------------------------
        # 3. High conflict → HOLD
        # -----------------------------
        if conflicts >= 2:
            return {"decision": "HOLD", "confidence": 40}

        # -----------------------------
        # 4. Neutral fallback
        # -----------------------------
        return {"decision": "HOLD", "confidence": 50}
