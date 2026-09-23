import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.risk_agent import RiskAgent

agent = RiskAgent("QQQ")

print("Fetching history...")
if agent.fetch_history():
    print("History fetched!\n")

    print("Volatility:")
    print(agent.volatility(), "\n")

    print("Max Drawdown:")
    print(agent.max_drawdown(), "\n")

    print("Risk Score:")
    print(agent.risk_score(), "\n")

else:
    print("Failed to fetch history.")
