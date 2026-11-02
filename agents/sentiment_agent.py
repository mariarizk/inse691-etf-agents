from agents.llm_client import LlmError
from config import AGENT_CONFIG

SENTIMENT_LABELS = ("Positive", "Neutral", "Negative")
SYSTEM_PROMPT = "You are a financial sentiment analyst. Reply with valid JSON only."


class SentimentAgent:
    """Classifies financial news with the LLM; falls back to price momentum when no news is available."""

    name = "sentiment"

    def __init__(self, llm_client=None, settings=None):
        self.llm = llm_client
        self.settings = settings or AGENT_CONFIG["sentiment"]

    def _build_prompt(self, article_text):

        return f"""
You are a financial sentiment analyst.

Analyze the following financial news article.

Classify sentiment as exactly one of:

- Positive
- Neutral
- Negative

Return ONLY valid JSON, with confidence as a number from 0 to 100:

{{
    "sentiment": "...",
    "confidence": 0,
    "reasoning": "..."
}}

Article:
{article_text}
"""

    def _call_llm(self, prompt):
        return self.llm.complete_json(SYSTEM_PROMPT, prompt)

    def analyze(self, price_df, article_text=None):
        if not article_text or self.llm is None:
            return self._from_price(price_df)

        try:
            return self._from_news(article_text)
        except (LlmError, TypeError, ValueError) as exc:
            result = self._from_price(price_df)
            result["reasoning"] += f" LLM unavailable: {exc}"
            return result

    def _from_news(self, article_text):
        result = self._call_llm(self._build_prompt(article_text))

        sentiment = str(result.get("sentiment", "")).strip().capitalize()
        if sentiment not in SENTIMENT_LABELS:
            raise ValueError(f"invalid sentiment {sentiment!r}")

        return {
            "sentiment": sentiment,
            "confidence": max(0, min(100, int(result.get("confidence", 50)))),
            "reasoning": str(result.get("reasoning", "")),
            "source": "llm",
        }

    def _from_price(self, price_df):
        recent_ret = price_df["Close"].pct_change().iloc[-1]

        if recent_ret > self.settings["positive_return"]:
            sentiment = "Positive"
        elif recent_ret < self.settings["negative_return"]:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "confidence": self.settings["rule_confidence"],
            "reasoning": f"No news analysed; latest daily return was {recent_ret:.2%}.",
            "source": "price",
        }
