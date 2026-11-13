from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.decision_agent import DecisionAgent
from agents.explanation_agent import ExplanationAgent


class ETFPipeline:

    def __init__(self):

        self.tech_agent = TechnicalAgent()
        self.sentiment_agent = SentimentAgent()
        self.risk_agent = RiskAgent()
        self.decision_agent = DecisionAgent()
        self.explanation_agent = ExplanationAgent()

    def run(self, price_df, article_text):

        # Non-LLM Agent
        technical_result = self.tech_agent.analyze(price_df)

        # LLM Guardrails
        try:

            sentiment_result = (
                self.sentiment_agent.analyze(article_text)
            )

            risk_result = (
                self.risk_agent.analyze(article_text)
            )

        except Exception as e:

            raise RuntimeError(
                f"Pipeline failed during Sentiment/Risk analysis: {e}"
            )

        # Rule-Based Agent
        decision_result = self.decision_agent.decide(
            technical_result,
            sentiment_result,
            risk_result
        )

        # Explanation Agent Guardrail
        try:

            explanation_result = (
                self.explanation_agent.analyze(
                    technical_result,
                    sentiment_result,
                    risk_result,
                    decision_result
                )
            )

        except Exception as e:

            raise RuntimeError(
                f"Pipeline failed during explanation generation: {e}"
            )

        return {
            "technical": technical_result,
            "sentiment": sentiment_result,
            "risk": risk_result,
            "decision": decision_result,
            "explanation": explanation_result
        }