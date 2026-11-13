import json
from backend.gemini_client import GeminiClient


class RiskAgent:

    def __init__(self):
        self.gemini = GeminiClient()

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

        Return ONLY valid JSON.

        Confidence must be an INTEGER between 0 and 100.

        {{
            "risk": "Low | Medium | High",
            "confidence": 0,
            "reasoning": "..."
        }}

        Article:
        {article_text}
        """


    def _call_llm(self, prompt):
        return self.gemini.generate(prompt)

    def analyze(self, article_text):

        if not article_text:
            raise ValueError(
                "RiskAgent received empty article."
            )

        if len(article_text.strip()) < 20:
            raise ValueError(
                "Article text too short."
            )

        prompt = self._build_prompt(article_text)

        response = self._call_llm(prompt)

        try:
            response = response.strip()

            if response.startswith("```json"):
                response = response.replace("```json", "", 1)

            if response.endswith("```"):
                response = response[:-3]


            result = json.loads(response)

            risk = result["risk"]
            confidence = result["confidence"]

            allowed_risk = [
                "Low",
                "Medium",
                "High"
            ]

            if risk not in allowed_risk:

                raise ValueError(
                    f"Invalid risk level: {risk}"
                )

            if not isinstance(confidence, (int, float)):
                raise ValueError(
                    "Confidence must be numeric."
                )

            # Reject decimal confidence values
            if confidence <= 1:
                raise ValueError(
                    "Confidence appears to be returned as a decimal instead of 0-100."
                )

            if confidence < 0 or confidence > 100:
                raise ValueError(
                    "Confidence must be between 0 and 100."
                )

            return {
                "risk": risk,
                "confidence": confidence,
                "reasoning": result["reasoning"]
            }

        except Exception as e:

            raise ValueError(
                f"RiskAgent invalid LLM response: {e}"
            )