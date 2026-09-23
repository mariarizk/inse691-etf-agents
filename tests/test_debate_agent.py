import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.debate_agent import DebateAgent
from agents.fundamental_agent import FundamentalAgent
from agents.technical_agent import TechnicalAgent
from agents.risk_agent import RiskAgent
from agents.sentiment_agent import SentimentAgent
from agents.diversification_agent import DiversificationAgentV2

# Metadata for Diversification Agent v2
TICKER_META = {
    "QQQ":  {"sector": "Tech", "leverage": 1},
    "SPY":  {"sector": "Broad", "leverage": 1},
    "TQQQ": {"sector": "Tech", "leverage": 3},
    "SQQQ": {"sector": "Tech", "leverage": -3},
}

# Instantiate agents
fund_agent = FundamentalAgent("QQQ")
tech_agent = TechnicalAgent("QQQ")
risk_agent = RiskAgent("QQQ")
sent_agent = SentimentAgent()
div_agent = DiversificationAgentV2(["QQQ", "SPY", "TQQQ", "SQQQ"], TICKER_META)

print("Fetching data...")

# FUNDAMENTAL
fund_agent.fetch_data()

# TECHNICAL
tech_agent.fetch_history()
tech_agent.compute_indicators()

# RISK  (THIS WAS THE BUG)
risk_agent.fetch_history()

# SENTIMENT
sent_agent.fetch_news()

# DIVERSIFICATION
div_agent.fetch_history()

# Summaries
fund_summary = fund_agent.summary()
tech_summary = tech_agent.summary()
risk_summary = {
    "volatility": risk_agent.volatility(),
    "max_drawdown": risk_agent.max_drawdown(),
    "risk_score": risk_agent.risk_score(),
    "risk_level": "High" if risk_agent.risk_score() >= 3 else "Moderate"
}
sent_summary = sent_agent.summary()
div_summary = div_agent.summary()

# Debate Agent
debate = DebateAgent(
    fundamental=fund_summary,
    technical=tech_summary,
    risk=risk_summary,
    sentiment=sent_summary,
    diversification=div_summary
)

print("\n=== Debate Summary ===")
summary = debate.debate_summary()

for key, value in summary.items():
    print(f"{key}:")
    if isinstance(value, list):
        for item in value:
            print(f"  - {item}")
    else:
        print(f"  {value}")
    print()
