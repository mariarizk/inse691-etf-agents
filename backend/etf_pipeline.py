from agents.blackboard import Blackboard
from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.decision_agent import ANALYST_AGENTS, DecisionAgent


class ETFPipeline:
    """Runs the analyst agents, shares their results on a blackboard, then decides."""

    def __init__(self, price_df):
        self.price_df = price_df
        self.blackboard = Blackboard()

        self.analysts = (TechnicalAgent(), SentimentAgent(), RiskAgent())
        self.dec_agent = DecisionAgent()

    def run(self):
        for agent in self.analysts:
            self.blackboard.write(agent.name, agent.analyze(self.price_df))

        missing = self.blackboard.missing(ANALYST_AGENTS)
        if missing:
            raise RuntimeError(f"Decision blocked, missing agent outputs: {missing}")

        decision = self.dec_agent.decide_from_blackboard(self.blackboard)
        self.blackboard.write(self.dec_agent.name, decision)

        return dict(self.blackboard.all())
