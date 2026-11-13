import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from agents.decision_agent import DecisionAgent

agent = DecisionAgent()

technical = "bullish"

sentiment = {
    "sentiment": "Positive",
    "confidence": 90,
    "reasoning": "Strong outlook."
}

risk = {
    "risk": "Low",
    "confidence": 85,
    "reasoning": "Stable market."
}

result = agent.decide(
    technical,
    sentiment,
    risk
)

print("\n=== Decision Agent Test ===\n")
print(result)

assert result["action"] == 1

print("\nPASS")