class RiskAgent:
    def analyze(self, price_df):
        vol = price_df["Close"].pct_change().rolling(20).std().iloc[-1]

        if vol < 0.01:
            return "low"
        elif vol < 0.02:
            return "medium"
        else:
            return "high"
