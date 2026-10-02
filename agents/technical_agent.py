class TechnicalAgent:
    def analyze(self, price_df):
        short_ma = price_df["Close"].rolling(10).mean().iloc[-1]
        long_ma = price_df["Close"].rolling(30).mean().iloc[-1]

        if short_ma > long_ma:
            return "bullish"
        elif short_ma < long_ma:
            return "bearish"
        else:
            return "neutral"
