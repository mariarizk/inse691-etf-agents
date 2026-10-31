import json

from agents.llm.client import LlmError
from agents.llm.prompts import NEWS_SENTIMENT_SYSTEM
from agents.llm.signals import NEWS_AGENT

NEWS_SIGNALS = ("positive", "neutral", "negative")


def _neutral(note, headline_count=0):
    return {
        "signal": "neutral",
        "score": 0.0,
        "summary": "",
        "headline_count": headline_count,
        "note": note,
    }


class NewsSentimentAgent:
    """Scores the tone of recent QQQ headlines with the LLM."""

    name = NEWS_AGENT

    def __init__(self, client):
        self.client = client

    def analyze(self, headlines):
        if not headlines:
            return _neutral("No headlines available.")

        try:
            result = self.client.complete_json(NEWS_SENTIMENT_SYSTEM, json.dumps(headlines, indent=2))
            signal = str(result.get("signal", "")).strip().lower()
            if signal not in NEWS_SIGNALS:
                raise LlmError(f"News analyst returned an invalid signal: {signal!r}")
            score = max(-1.0, min(1.0, float(result.get("score", 0))))
        except (LlmError, TypeError, ValueError) as exc:
            return _neutral(f"News sentiment unavailable: {exc}", len(headlines))

        return {
            "signal": signal,
            "score": score,
            "summary": str(result.get("summary", "")),
            "headline_count": len(headlines),
            "note": None,
        }
