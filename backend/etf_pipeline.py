from agents.blackboard import Blackboard
from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.decision_agent import ANALYST_AGENTS, DecisionAgent
from agents.explanation_agent import ExplanationAgent


class ETFPipeline:
    """Runs the five agents; they communicate only through a shared blackboard."""

    def __init__(self, llm_client=None):

        self.tech_agent = TechnicalAgent()
        self.sentiment_agent = SentimentAgent(llm_client)
        self.risk_agent = RiskAgent(llm_client)
        self.decision_agent = DecisionAgent()
        self.explanation_agent = ExplanationAgent(llm_client) if llm_client else None

    def run(self, price_df, article_text=None, explain=False):

        board = Blackboard()

        board.write(self.tech_agent.name, self.tech_agent.analyze(price_df))
        board.write(self.sentiment_agent.name, self.sentiment_agent.analyze(price_df, article_text))
        board.write(self.risk_agent.name, self.risk_agent.analyze(price_df, article_text))

        missing = board.missing(ANALYST_AGENTS)
        if missing:
            raise RuntimeError(f"Decision blocked, missing agent outputs: {missing}")

        board.write(self.decision_agent.name, self.decision_agent.decide_from_blackboard(board))

        if explain and self.explanation_agent:
            board.write(self.explanation_agent.name, self.explanation_agent.explain(board.all()))

        return {**board.all(), "log": board.history()}
