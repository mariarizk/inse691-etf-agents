class DecisionAgent:

    def decide(self, technical, sentiment, risk):

        sentiment_label = sentiment["sentiment"]
        sentiment_confidence = sentiment["confidence"]

        risk_label = risk["risk"]
        risk_confidence = risk["confidence"]

        # Ignore weak LLM outputs
        if sentiment_confidence < 60:
            sentiment_label = "Neutral"

        if risk_confidence < 60:
            risk_label = "Medium"

        # SELL
        if (
            technical == "bearish"
            or sentiment_label == "Negative"
            or risk_label == "High"
        ):
            return {
                "action": -1,
                "reasoning": (
                    f"Technical={technical}, "
                    f"Sentiment={sentiment_label}, "
                    f"Risk={risk_label}"
                )
            }

        # BUY
        if (
            technical == "bullish"
            and sentiment_label == "Positive"
            and risk_label == "Low"
        ):
            return {
                "action": 1,
                "reasoning": (
                    f"Technical={technical}, "
                    f"Sentiment={sentiment_label}, "
                    f"Risk={risk_label}"
                )
            }

        # HOLD
        return {
            "action": 0,
            "reasoning": (
                f"Mixed signals: "
                f"Technical={technical}, "
                f"Sentiment={sentiment_label}, "
                f"Risk={risk_label}"
            )
        }