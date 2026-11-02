from agents.llm_client import LlmError
from config import AGENT_CONFIG

RISK_LABELS = ("Low", "Medium", "High")
SYSTEM_PROMPT = "You are a financial risk analyst. Reply with valid JSON only."


class RiskAgent:
    """Classifies investment risk from news and recent volatility with the LLM; falls back to volatility alone."""

    name = "risk"

    def __init__(self, llm_client=None, settings=None):
        self.llm = llm_client
        self.settings = settings or AGENT_CONFIG["risk"]

    def _build_prompt(self, article_text, volatility):

        return f"""
You are a financial risk analyst.

Analyze the following financial news article.

Classify the investment risk level as exactly one of:

- Low
- Medium
- High

Consider factors such as:

- Regulatory action
- Litigation
- Earnings uncertainty
- Revenue risk
- Market volatility
- Geopolitical exposure
- Supply chain issues
- Competitive threats

Current 20-day volatility of QQQ daily returns: {volatility:.2%}

Return ONLY valid JSON, with confidence as a number from 0 to 100:

{{
    "risk": "...",
    "confidence": 0,
    "reasoning": "..."
}}

Article:
{article_text}
"""

    def _call_llm(self, prompt):
        return self.llm.complete_json(SYSTEM_PROMPT, prompt)

    def _volatility(self, price_df):
        return float(price_df["Close"].pct_change().rolling(self.settings["window"]).std().iloc[-1])

    def analyze(self, price_df, article_text=None):
        volatility = self._volatility(price_df)
        if not article_text or self.llm is None:
            return self._from_volatility(volatility)

        try:
            return self._from_news(article_text, volatility)
        except (LlmError, TypeError, ValueError) as exc:
            result = self._from_volatility(volatility)
            result["reasoning"] += f" LLM unavailable: {exc}"
            return result

    def _from_news(self, article_text, volatility):
        result = self._call_llm(self._build_prompt(article_text, volatility))

        risk = str(result.get("risk", "")).strip().capitalize()
        if risk not in RISK_LABELS:
            raise ValueError(f"invalid risk {risk!r}")

        return {
            "risk": risk,
            "confidence": max(0, min(100, int(result.get("confidence", 50)))),
            "reasoning": str(result.get("reasoning", "")),
            "daily_volatility": volatility,
            "source": "llm",
        }

    def _from_volatility(self, volatility):
        if volatility < self.settings["low_volatility"]:
            risk = "Low"
        elif volatility < self.settings["medium_volatility"]:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "risk": risk,
            "confidence": self.settings["rule_confidence"],
            "reasoning": f"No news analysed; 20-day volatility is {volatility:.2%}.",
            "daily_volatility": volatility,
            "source": "price",
        }
