class DebateAgent:
    def __init__(self, fundamental, technical, risk, sentiment, diversification):
        self.fundamental = fundamental
        self.technical = technical
        self.risk = risk
        self.sentiment = sentiment
        self.diversification = diversification

    def bullish_arguments(self):
        args = []

        # Fundamentals
        if self.fundamental.get("rating") == "Bullish":
            args.append("Fundamental Agent sees strong valuation and financial health.")

        # Technicals
        if self.technical.get("signal") == "BUY":
            args.append("Technical Agent detects upward momentum and a buy signal.")

        # Sentiment
        if self.sentiment.get("classification") == "Positive sentiment":
            args.append("Sentiment Agent reports positive market tone.")

        # Diversification
        if self.diversification.get("final_diversification_score", 0) >= 6:
            args.append("Diversification Agent indicates strong diversification support.")

        return args

    def bearish_arguments(self):
        args = []

        # Fundamentals
        if self.fundamental.get("rating") == "Bearish":
            args.append("Fundamental Agent warns of weak valuation or financial deterioration.")

        # Technicals
        if self.technical.get("signal") == "SELL":
            args.append("Technical Agent detects downward momentum and a sell signal.")

        # Sentiment
        if self.sentiment.get("classification") == "Negative sentiment":
            args.append("Sentiment Agent reports negative market tone.")

        # Risk
        if self.risk.get("risk_level") == "High":
            args.append("Risk Agent flags high volatility or drawdown risk.")

        # Diversification
        if self.diversification.get("final_diversification_score", 0) <= 3:
            args.append("Diversification Agent indicates poor diversification and concentration risk.")

        return args

    def conflict_analysis(self):
        bullish = self.bullish_arguments()
        bearish = self.bearish_arguments()

        conflicts = []

        if bullish and bearish:
            conflicts.append("Agents disagree: bullish and bearish signals detected.")
        if self.fundamental.get("rating") != self.technical.get("signal"):
            conflicts.append("Fundamental and Technical Agents disagree.")
        if self.sentiment.get("classification") == "Neutral sentiment":
            conflicts.append("Sentiment Agent is neutral, reducing conviction.")
        if self.risk.get("risk_level") == "High" and bullish:
            conflicts.append("Risk Agent contradicts bullish arguments.")

        return conflicts

    def debate_summary(self):
        return {
            "bullish_arguments": self.bullish_arguments(),
            "bearish_arguments": self.bearish_arguments(),
            "conflicts": self.conflict_analysis()
        }
