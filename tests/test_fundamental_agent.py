import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.fundamental_agent import FundamentalAgent

agent = FundamentalAgent("QQQ")

print("Fetching data...")
if agent.fetch_data():
    print("Data fetched successfully!")

    print("\nBasic ratios:")
    print(agent.get_basic_ratios())

    print("\nAnalysis:")
    print(agent.analyze())
else:
    print("Failed to fetch data.")
