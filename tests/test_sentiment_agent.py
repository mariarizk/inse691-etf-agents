import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from agents.sentiment_agent import SentimentAgent

agent = SentimentAgent()

article = """
Microsoft reported stronger-than-expected earnings and
raised guidance for next quarter. Analysts expect growth
to continue through the year.
"""

result = agent.analyze(article)

print("\n=== Sentiment Agent Test ===\n")
print(result)

assert result["sentiment"] in [
    "Positive",
    "Neutral",
    "Negative"
]

assert 0 <= result["confidence"] <= 100

assert len(result["reasoning"]) > 0

print("\nPASS")