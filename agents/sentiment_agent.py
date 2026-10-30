from config import AGENT_CONFIG


class SentimentAgent:
    name = "sentiment"

    def __init__(self, settings=None):
        self.settings = settings or AGENT_CONFIG["sentiment"]

    def analyze(self, price_df):
        recent_ret = price_df["Close"].pct_change().iloc[-1]

        if recent_ret > self.settings["positive_return"]:
            signal = "positive"
        elif recent_ret < self.settings["negative_return"]:
            signal = "negative"
        else:
            signal = "neutral"

        return {
            "signal": signal,
            "last_return": float(recent_ret),
        }
