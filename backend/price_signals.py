"""Price-based Sentiment and Risk signals for historic backtests.

Matches the design: backtest uses historic QQQ prices without live news
or LLM calls. Sentiment uses the latest daily return; Risk uses 20-day
return volatility.
"""


def sentiment_from_price(price_df):
    """Classify sentiment from the latest daily return."""
    if len(price_df) < 2:
        return {
            "tool_used": "price_based_sentiment",
            "sentiment": "Neutral",
            "confidence": 60,
            "reasoning": "Insufficient price history for return-based sentiment.",
            "source": "price",
        }

    daily_return = price_df["Close"].pct_change().iloc[-1]

    if daily_return > 0.01:
        sentiment = "Positive"
        reasoning = (
            f"Latest daily return {daily_return:.2%} is above +1%."
        )
    elif daily_return < -0.01:
        sentiment = "Negative"
        reasoning = (
            f"Latest daily return {daily_return:.2%} is below -1%."
        )
    else:
        sentiment = "Neutral"
        reasoning = (
            f"Latest daily return {daily_return:.2%} is within ±1%."
        )

    return {
        "tool_used": "price_based_sentiment",
        "sentiment": sentiment,
        "confidence": 70,
        "reasoning": reasoning,
        "source": "price",
    }


def risk_from_price(price_df, window=20):
    """Classify risk from rolling daily-return volatility."""
    if len(price_df) < 2:
        return {
            "tool_used": "price_based_risk",
            "risk": "Medium",
            "confidence": 60,
            "reasoning": "Insufficient price history for volatility-based risk.",
            "source": "price",
        }

    returns = price_df["Close"].pct_change().dropna()
    lookback = min(window, len(returns))
    volatility = returns.iloc[-lookback:].std()

    if volatility < 0.01:
        risk = "Low"
        reasoning = (
            f"{lookback}-day volatility {volatility:.2%} is below 1%."
        )
    elif volatility < 0.02:
        risk = "Medium"
        reasoning = (
            f"{lookback}-day volatility {volatility:.2%} is between 1% and 2%."
        )
    else:
        risk = "High"
        reasoning = (
            f"{lookback}-day volatility {volatility:.2%} is at or above 2%."
        )

    return {
        "tool_used": "price_based_risk",
        "risk": risk,
        "confidence": 70,
        "reasoning": reasoning,
        "source": "price",
    }
