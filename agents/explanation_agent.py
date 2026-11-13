import json
from backend.gemini_client import GeminiClient


class ExplanationAgent:

    def __init__(self):
        self.gemini = GeminiClient()

    def _build_prompt(
        self,
        technical,
        sentiment,
        risk,
        decision
    ):

        return f"""
        You are a financial analyst.

        Technical Signal:
        {technical}

        Sentiment:
        {sentiment['sentiment']}
        Confidence: {sentiment['confidence']}

        Risk:
        {risk['risk']}
        Confidence: {risk['confidence']}

        Decision:
        {decision['action']}

        Generate a concise explanation for this recommendation.

        Return ONLY valid JSON:

        {{
            "explanation": "...",
            "consistency": true
        }}
        """

    def _call_llm(self, prompt):
        return self.gemini.generate(prompt)
    
    def analyze(
        self,
        technical,
        sentiment,
        risk,
        decision
    ):

        prompt = self._build_prompt(
            technical,
            sentiment,
            risk,
            decision
        )

        response = self._call_llm(prompt)

        try:
            response = response.strip()

            if response.startswith("```json"):
                response = response.replace("```json", "", 1)

            if response.endswith("```"):
                response = response[:-3]


            result = json.loads(response)

            if "explanation" not in result:
                raise ValueError(
                    "Missing explanation field."
                )

            if "consistency" not in result:
                raise ValueError(
                    "Missing consistency field."
                )

            explanation = result["explanation"]

            if not isinstance(explanation, str):
                raise ValueError(
                    "Explanation must be a string."
                )

            if len(explanation.strip()) < 20:
                raise ValueError(
                    "Explanation too short."
                )

            if not isinstance(result["consistency"], bool):
                raise ValueError(
                    "Consistency must be boolean."
                )

            return {
                "explanation": explanation,
                "consistency": result["consistency"]
            }

        except Exception as e:

            raise ValueError(
                f"ExplanationAgent invalid LLM response: {e}"
            )