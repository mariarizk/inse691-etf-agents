import json


class RiskAgent:

    def __init__(self):
        pass

    def _build_prompt(self, article_text):

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

Return ONLY valid JSON:

{{
    "risk": "...",
    "confidence": 0,
    "reasoning": "..."
}}

Article:
{article_text}
"""

    def _call_llm(self, prompt):
        """
        Placeholder.

        Replace with GPT/OpenAI call.
        """

        raise NotImplementedError(
            "Replace with OpenAI API implementation."
        )

    def analyze(self, article_text):

        prompt = self._build_prompt(article_text)

        response = self._call_llm(prompt)

        try:

            result = json.loads(response)

            return {
                "risk": result.get("risk", "Medium"),
                "confidence": result.get("confidence", 50),
                "reasoning": result.get("reasoning", "")
            }

        except Exception as e:
            raise Exception(
                f"RiskAgent failed to parse LLM response: {e}"
            )