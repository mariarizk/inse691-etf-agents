from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.decision_agent import DecisionAgent
from agents.explanation_agent import ExplanationAgent
from agents.blackboard import Blackboard


class ETFPipeline:

    def __init__(self):

        self.tech_agent = TechnicalAgent()
        self.sentiment_agent = SentimentAgent()
        self.risk_agent = RiskAgent()
        self.decision_agent = DecisionAgent()
        self.explanation_agent = ExplanationAgent()
        self.blackboard = Blackboard()

    def run(
        self,
        price_df,
        article_text
    ):

        # ==================================================
        # TECHNICAL AGENT
        # ==================================================

        technical_result = self.tech_agent.analyze(
            price_df
        )

        self.blackboard.write(
            "technical",
            technical_result
        )

        # ==================================================
        # SENTIMENT AGENT
        # ==================================================

        try:

            sentiment_result = (
                self.sentiment_agent.analyze(
                    article_text
                )
            )

        except Exception as e:

            print(
                f"Sentiment fallback activated: {e}"
            )

            sentiment_result = {
                "tool_used": "pipeline_fallback",
                "sentiment": "Neutral",
                "confidence": 0,
                "reasoning":
                    "Pipeline fallback response."
            }

        self.blackboard.write(
            "sentiment",
            sentiment_result
        )

        # ==================================================
        # RISK AGENT
        # ==================================================

        try:

            risk_result = (
                self.risk_agent.analyze(
                    article_text
                )
            )

        except Exception as e:

            print(
                f"Risk fallback activated: {e}"
            )

            risk_result = {
                "tool_used": "pipeline_fallback",
                "risk": "Medium",
                "confidence": 0,
                "reasoning":
                    "Pipeline fallback response."
            }

        self.blackboard.write(
            "risk",
            risk_result
        )

        # ==================================================
        # DECISION AGENT
        # ==================================================

        decision_result = (
            self.decision_agent.decide(
                technical_result,
                sentiment_result,
                risk_result
            )
        )

        self.blackboard.write(
            "decision",
            decision_result
        )

        # ==================================================
        # EXPLANATION AGENT
        # ==================================================

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

            explanation_result = {
                "tool_used": "pipeline_fallback",
                "explanation":
                    "Explanation service temporarily unavailable.",
                "consistency": False,
                "error": str(e)
            }

        self.blackboard.write(
            "explanation",
            explanation_result
        )

        # ==================================================
        # PIPELINE RESULT
        # ==================================================

        final_result = {
            "technical": technical_result,
            "sentiment": sentiment_result,
            "risk": risk_result,
            "decision": decision_result,
            "explanation": explanation_result
        }

        self.blackboard.write(
            "pipeline_result",
            final_result
        )

        return final_result