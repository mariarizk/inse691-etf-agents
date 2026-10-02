from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.decision_agent import DecisionAgent

class ETFPipeline:
    def __init__(self, price_df, headlines):
        self.price_df = price_df
        self.headlines = headlines

        self.tech_agent = TechnicalAgent()
        self.sent_agent = SentimentAgent()
        self.risk_agent = RiskAgent()
        self.dec_agent = DecisionAgent()

    def run(self):
        tech = self.tech_agent.analyze(self.price_df)
        sentiment = self.sent_agent.analyze(self.price_df)
        risk = self.risk_agent.analyze(self.price_df)

        decision = self.dec_agent.decide(tech, sentiment, risk)

        return {
            "technical": tech,
            "sentiment": sentiment,
            "risk": risk,
            "decision": {"action": decision}

        }
