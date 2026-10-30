from config import AGENT_CONFIG


class RiskAgent:
    name = "risk"

    def __init__(self, settings=None):
        self.settings = settings or AGENT_CONFIG["risk"]

    def analyze(self, price_df):
        vol = price_df["Close"].pct_change().rolling(self.settings["window"]).std().iloc[-1]

        if vol < self.settings["low_volatility"]:
            signal = "low"
        elif vol < self.settings["medium_volatility"]:
            signal = "medium"
        else:
            signal = "high"

        return {
            "signal": signal,
            "daily_volatility": float(vol),
        }
