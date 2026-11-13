import json
from backend.gemini_client import GeminiClient


class SentimentAgent:

    def __init__(self):
        self.gemini = GeminiClient()


    def _build_prompt(self, article_text):

        return f"""
        You are a financial sentiment analyst.

        Analyze the following financial news article.

        Classify sentiment as exactly one of:

        - Positive
        - Neutral
        - Negative
        Return ONLY valid JSON.

        Confidence must be an integer between 0 and 100.

        {{
            "sentiment": "Positive | Neutral | Negative",
            "confidence": 0,
            "reasoning": "One concise explanation."
        }}

        Article:
        {article_text}
        """




    def _call_llm(self, prompt):
        return self.gemini.generate(prompt)
    

    def analyze(self, article_text):

        if not article_text:
            raise ValueError(
                "SentimentAgent received empty article."
            )

        if len(article_text.strip()) < 20:
            raise ValueError(
                "Article text too short."
            )

        prompt = self._build_prompt(article_text)

        response = self._call_llm(prompt)

        try:
            response = self._call_llm(prompt)

            response = response.strip()

            if response.startswith("```json"):
                response = response.replace("```json", "", 1)

            if response.endswith("```"):
                response = response[:-3]

            response = response.strip()

            result = json.loads(response)

            sentiment = result["sentiment"]
            confidence = result["confidence"]

            allowed_sentiments = [
                "Positive",
                "Neutral",
                "Negative"
            ]

            if sentiment not in allowed_sentiments:

                raise ValueError(
                    f"Invalid sentiment: {sentiment}"
                )

            if not isinstance(confidence, (int, float)):
                raise ValueError(
                    "Confidence must be numeric."
                )

            if confidence < 0 or confidence > 100:
                raise ValueError(
                    "Confidence must be between 0 and 100."
                )
            if confidence <= 5:
                raise ValueError(
                    f"Suspicious confidence value returned: {confidence}"
                )
            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "reasoning": result["reasoning"]
            }

        except Exception as e:

            raise ValueError(
                f"SentimentAgent invalid LLM response: {e}"
            )