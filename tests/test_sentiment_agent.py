import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.sentiment_agent import SentimentAgent

agent = SentimentAgent()

print("Fetching news...")
if agent.fetch_news():
    print("News fetched!\n")

    print("Headline Sentiment Score:")
    print(agent.headline_sentiment(), "\n")

    print("Sentiment Classification:")
    print(agent.classify_sentiment(), "\n")

else:
    print("Failed to fetch news.")
