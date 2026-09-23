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
        # 1. Strong BUY override
        # -----------------------------
        if technical_signal == "BUY" and bullish > bearish:
            return {"decision": "BUY", "confidence": 70}

        # -----------------------------
        # 2. Strong SELL override
        # -----------------------------
        if technical_signal == "SELL" and bearish > bullish:
            return {"decision": "SELL", "confidence": 70}

        # -----------------------------
        # 3. Moderate BUY conditions
        # -----------------------------
        if bullish > bearish and conflicts <= 1:
            if sentiment_score > 0 and risk_score <= 3:
                return {"decision": "BUY", "confidence": 55}

        # -----------------------------
        # 4. Moderate SELL conditions
        # -----------------------------
        if bearish > bullish and conflicts <= 1:
            if sentiment_score < 0 or risk_score >= 4:
                return {"decision": "SELL", "confidence": 55}

        # -----------------------------
        # 5. High conflict → HOLD
        # -----------------------------
        if conflicts >= 2:
            return {"decision": "HOLD", "confidence": 40}

        # -----------------------------
        # 6. Neutral fallback
        # -----------------------------
        return {"decision": "HOLD", "confidence": 50}
