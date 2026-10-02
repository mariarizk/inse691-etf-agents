import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.sentiment_agent import SentimentAgent

agent = SentimentAgent()

print("Fetching news...")
if agent.fetch_news("QQQ"):
    print("News fetched!")
    print("Sentiment Score:", agent.headline_sentiment())
    print("Sentiment Classification:", agent.classify_sentiment())
else:
    print("Failed to fetch news.")

