class DecisionAgent:

    def decide(
        self,
        technical,
        sentiment,
        risk
    ):

        # Allowed values only
        allowed_technical = [
            "bullish",
            "neutral",
            "bearish"
        ]

        allowed_sentiment = [
            "Positive",
            "Neutral",
            "Negative"
        ]

        allowed_risk = [
            "Low",
            "Medium",
            "High"
        ]

        # Input validation

        if technical not in allowed_technical:

            raise ValueError(
                f"Invalid technical signal: {technical}"
            )

        sentiment_label = sentiment["sentiment"]
        sentiment_confidence = sentiment["confidence"]

        risk_label = risk["risk"]
        risk_confidence = risk["confidence"]

        if sentiment_label not in allowed_sentiment:

            raise ValueError(
                f"Invalid sentiment label: "
                f"{sentiment_label}"
            )

        if risk_label not in allowed_risk:

            raise ValueError(
                f"Invalid risk label: "
                f"{risk_label}"
            )

        # Confidence validation

        if not (
            0 <= sentiment_confidence <= 100
        ):

            raise ValueError(
                "Invalid sentiment confidence."
            )

        if not (
            0 <= risk_confidence <= 100
        ):

            raise ValueError(
                "Invalid risk confidence."
            )

        # Low-confidence guardrail

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
                "action_label": "SELL",
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
                "action_label": "BUY",
                "reasoning": (
                    f"Technical={technical}, "
                    f"Sentiment={sentiment_label}, "
                    f"Risk={risk_label}"
                )
            }

        # HOLD

        return {
            "action": 0,
            "action_label": "HOLD",
            "reasoning": (
                f"Mixed signals: "
                f"Technical={technical}, "
                f"Sentiment={sentiment_label}, "
                f"Risk={risk_label}"
            )
        }