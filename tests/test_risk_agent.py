import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from agents.risk_agent import RiskAgent

agent = RiskAgent()

article = """
NVIDIA is facing increased regulatory scrutiny regarding
AI chip exports. Analysts believe additional restrictions
could impact future revenue growth.
"""

result = agent.analyze(article)

print("\n=== Risk Agent Test ===\n")
print(result)

assert result["risk"] in [
    "Low",
    "Medium",
    "High"
]

assert 0 <= result["confidence"] <= 100

assert len(result["reasoning"]) > 0

print("\nPASS")