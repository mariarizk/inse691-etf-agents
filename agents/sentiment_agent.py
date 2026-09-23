import requests
from textblob import TextBlob

TOP_QQQ_HOLDINGS = ["AAPL", "MSFT", "AMZN", "NVDA", "META", "TSLA"]

class SentimentAgent:
    def __init__(self):
        self.news = []

    def fetch_news(self):
        try:
            url = f"https://api.marketaux.com/v1/news/all?symbols={','.join(TOP_QQQ_HOLDINGS)}&filter_entities=true&language=en&api_token=0NaVLfxxbmiNj091dDOzgHRqoZrMRxcxfY9a9MGA"
            response = requests.get(url).json()

            if "data" in response:
                self.news = response["data"]
                return True

            self.news = []
            return False

        except Exception as e:
            print("Error fetching news:", e)
            return False


    def headline_sentiment(self):
        if not self.news:
            return None

        scores = []
        for item in self.news[:20]:
            headline = item.get("title", "")
            blob = TextBlob(headline)
            scores.append(blob.sentiment.polarity)

        if not scores:
            return None

        return sum(scores) / len(scores)


    def classify_sentiment(self):
        score = self.headline_sentiment()
        if score is None:
            return "No sentiment data."

        if score > 0.2:
            return "Positive sentiment"
        elif score < -0.2:
            return "Negative sentiment"
        else:
            return "Neutral sentiment"
        
    def summary(self):
        return {
            "articles": self.articles if hasattr(self, "articles") else None,
            "sentiment_score": self.sentiment_score if hasattr(self, "sentiment_score") else None,
            "classification": self.classification if hasattr(self, "classification") else "Neutral sentiment"
        }
