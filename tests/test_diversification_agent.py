import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.diversification_agent import DiversificationAgentV2

TICKER_META = {
    "QQQ":  {"sector": "Tech", "leverage": 1},
    "SPY":  {"sector": "Broad", "leverage": 1},
    "TQQQ": {"sector": "Tech", "leverage": 3},
    "SQQQ": {"sector": "Tech", "leverage": -3},
}

tickers = ["QQQ", "SPY", "TQQQ", "SQQQ"]
agent = DiversificationAgentV2(tickers, TICKER_META)

print("Fetching history...")
if agent.fetch_history():
    print("History fetched!\n")

    print("Correlation Matrix:")
    print(agent.correlation_matrix(), "\n")

    print("Summary:")
    summary = agent.summary()
    for k, v in summary.items():
        print(f"{k}: {v}")
else:
    print("Failed to fetch history.")
