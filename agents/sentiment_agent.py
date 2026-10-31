import json


class SentimentAgent:

    def __init__(self):
        pass

    def _build_prompt(self, article_text):

        return f"""
You are a financial sentiment analyst.

Analyze the following financial news article.

Classify sentiment as exactly one of:

- Positive
- Neutral
- Negative

Return ONLY valid JSON:

{{
    "sentiment": "...",
    "confidence": 0,
    "reasoning": "..."
}}

Article:
{article_text}
"""

    def _call_llm(self, prompt):
        """
        Placeholder.

        Your partner will replace this section with
        the OpenAI API call.
        """

        raise NotImplementedError(
            "Replace this with OpenAI API call."
        )

    def analyze(self, article_text):

        prompt = self._build_prompt(article_text)

        response = self._call_llm(prompt)

        try:
            result = json.loads(response)

            return {
                "sentiment": result.get("sentiment", "Neutral"),
                "confidence": result.get("confidence", 50),
                "reasoning": result.get("reasoning", "")
            }

        except json.JSONDecodeError:
            raise ValueError(
                f"SentimentAgent received invalid JSON from LLM: {response}"
            )