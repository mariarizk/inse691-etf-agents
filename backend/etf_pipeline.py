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


    def run(self, price_df, article_text):

        # Non-LLM Agent
        technical_result = self.tech_agent.analyze(price_df)
        self.blackboard.write(
            "technical",
            technical_result
        )


        # LLM Guardrails
        try:

            sentiment_result = (
                self.sentiment_agent.analyze(article_text)
            )
            self.blackboard.write(
                "sentiment",
                sentiment_result
            )

                   

            risk_result = (
                self.risk_agent.analyze(article_text)
            )
            self.blackboard.write(
                "risk",
                risk_result
            )

      
        except Exception as e:

            print(
                f"Sentiment/Risk fallback activated: {e}"
            )

            sentiment_result = {
                "sentiment": "Neutral",
                "confidence": 0,
                "reasoning":
                    "Gemini unavailable. Fallback response."
            }

            risk_result = {
                "risk": "Medium",
                "confidence": 0,
                "reasoning":
                    "Gemini unavailable. Fallback response."
            }

            self.blackboard.write(
                "sentiment",
                sentiment_result
            )

            self.blackboard.write(
                "risk",
                risk_result
            )

        # Rule-Based Agent
        decision_result = self.decision_agent.decide(
            technical_result,
            sentiment_result,
            risk_result
        )
        self.blackboard.write(
            "decision",
            decision_result
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

            explanation_result = {
                "explanation":
                    "Explanation service temporarily unavailable.",
                "consistency": False,
                "error": str(e)
            }
            
        self.blackboard.write(
            "explanation",
            explanation_result
        )
      

        return {
            "technical": technical_result,
            "sentiment": sentiment_result,
            "risk": risk_result,
            "decision": decision_result,
            "explanation": explanation_result
        }