import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from agents.explanation_agent import ExplanationAgent

agent = ExplanationAgent()

technical = "bullish"

sentiment = {
    "sentiment": "Positive",
    "confidence": 88,
    "reasoning": "Strong earnings growth."
}

risk = {
    "risk": "Low",
    "confidence": 84,
    "reasoning": "Low volatility."
}

decision = {
    "action": 1
}

result = agent.analyze(
    technical,
    sentiment,
    risk,
    decision
)

print("\n=== Explanation Agent Test ===\n")
print(result)

assert "explanation" in result

assert len(result["explanation"]) > 20

assert "consistency" in result

print("\nPASS")