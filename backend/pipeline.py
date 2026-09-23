from agents.fundamental_agent import FundamentalAgent
from agents.technical_agent import TechnicalAgent
from agents.risk_agent import RiskAgent
from agents.sentiment_agent import SentimentAgent
from agents.diversification_agent import DiversificationAgent
from agents.debate_agent import DebateAgent
from agents.decision_agent import DecisionAgent
import yfinance as yf


TICKER_META = {
    "QQQ": {"type": "non-leveraged"},
    "TQQQ": {"type": "leveraged-long"},
    "SQQQ": {"type": "leveraged-inverse"}
}

class ETFPipeline:
    def __init__(self, ticker, data=None):
        self.ticker = ticker

        if data is None:
            self.data = yf.download(ticker, start="2018-01-01", end="2024-01-01")
        else:
            self.data = data



    def run(self):

        # 1. Create metadata for diversification agent
        tickers = [self.ticker]
        meta = {
            self.ticker: {
                "sector": "Tech",
                "leverage": 1 if self.ticker == "QQQ" else 3 if self.ticker == "TQQQ" else -3
            }
        }

        # 2. Create agents
        fundamental_agent = FundamentalAgent(self.data)
        technical_agent = TechnicalAgent(self.ticker)
        technical_agent.fetch_history()
        technical_agent.compute_indicators()   # REQUIRED
        risk_agent = RiskAgent(self.ticker)
        risk_agent.fetch_history()  # load data
        sentiment_agent = SentimentAgent()
        diversification_agent = DiversificationAgent(tickers, meta)

        # 3. Run each agent → produce summaries
        fundamental_summary = fundamental_agent.summary()
        technical_summary = technical_agent.summary()
        risk_summary = risk_agent.summary()
        sentiment_summary = sentiment_agent.summary()
        diversification_summary = diversification_agent.summary()

        # 4. Debate Agent
        debate_agent = DebateAgent(
            fundamental_summary,
            technical_summary,
            risk_summary,
            sentiment_summary,
            diversification_summary
        )
        debate_summary = debate_agent.debate_summary()

        # 5. Decision Agent
        decision = DecisionAgent().decide(
            fundamental_summary,
            technical_summary,
            risk_summary,
            sentiment_summary,
            diversification_summary,
            debate_summary
        )

        # 6. Return everything
        return {
            "fundamental": fundamental_summary,
            "technical": technical_summary,
            "risk": risk_summary,
            "sentiment": sentiment_summary,
            "diversification": diversification_summary,
            "debate": debate_summary,
            "decision": decision
        }

