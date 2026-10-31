from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.decision_agent import DecisionAgent


class ETFPipeline:

    def __init__(self):

        self.tech_agent = TechnicalAgent()
        self.sentiment_agent = SentimentAgent()
        self.risk_agent = RiskAgent()
        self.decision_agent = DecisionAgent()

    def run(self, price_df, article_text):

        technical_result = self.tech_agent.analyze(price_df)

        sentiment_result = self.sentiment_agent.analyze(
            article_text
        )

        risk_result = self.risk_agent.analyze(
            article_text
        )

        decision_result = self.decision_agent.decide(
            technical_result,
            sentiment_result,
            risk_result
        )

        return {
            "technical": technical_result,
            "sentiment": sentiment_result,
            "risk": risk_result,
            "decision": decision_result
        }