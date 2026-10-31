from agents.risk_agent import RiskAgent

article = """
NVIDIA shares fell after regulators announced a new review
of AI chip exports to foreign markets. Analysts expect
additional restrictions to impact future revenue growth.
"""

agent = RiskAgent()

result = agent.analyze(article)

print("\n=== Risk Agent Output ===\n")
print(result)