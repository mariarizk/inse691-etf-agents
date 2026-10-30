from config import AGENT_CONFIG


class TechnicalAgent:
    name = "technical"

    def __init__(self, settings=None):
        self.settings = settings or AGENT_CONFIG["technical"]

    def analyze(self, price_df):
        close = price_df["Close"]
        short_ma = close.rolling(self.settings["short_window"]).mean().iloc[-1]
        long_ma = close.rolling(self.settings["long_window"]).mean().iloc[-1]

        if short_ma > long_ma:
            signal = "bullish"
        elif short_ma < long_ma:
            signal = "bearish"
        else:
            signal = "neutral"

        return {
            "signal": signal,
            "short_ma": float(short_ma),
            "long_ma": float(long_ma),
        }
