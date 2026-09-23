import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.technical_agent import TechnicalAgent

agent = TechnicalAgent("QQQ")

print("Fetching price history...")
if agent.fetch_history():
    print("History fetched successfully!\n")

    print("Moving Averages:")
    print(agent.moving_averages(), "\n")

    print("RSI:")
    print(agent.rsi(), "\n")

    print("MACD:")
    print(agent.macd(), "\n")

    print("Mean Reversion (Z-Score):")
    print(agent.mean_reversion(), "\n")

else:
    print("Failed to fetch history.")
