class SentimentAgent:
    def analyze(self, price_df):
        recent_ret = price_df["Close"].pct_change().iloc[-1]

        if recent_ret > 0.01:
            return "positive"
        elif recent_ret < -0.01:
            return "negative"
        else:
            return "neutral"
