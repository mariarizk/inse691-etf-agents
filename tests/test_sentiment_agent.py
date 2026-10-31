from agents.sentiment_agent import SentimentAgent

article = """
NVIDIA shares fell after regulators announced a new review
of AI chip exports. Analysts expect the restrictions to
reduce future revenue growth.
"""

agent = SentimentAgent()

result = agent.analyze(article)

print(result)