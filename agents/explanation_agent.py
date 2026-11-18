import json

from backend.gemini_client import GeminiClient


class ExplanationAgent:

    MIN_EXPLANATION_LENGTH = 250

    FORBIDDEN_TERMS = [
        "system prompt",
        "developer message",
        "hidden instructions",
        "internal prompt",
        "ignore previous instructions",
        "jailbreak",
        "override instructions"
    ]

    def __init__(self):
        self.gemini = GeminiClient()

    # =====================================================
    # EXPLANATION GENERATION
    # =====================================================

    def _build_prompt(
        self,
        technical,
        sentiment,
        risk,
        decision
    ):

        return f"""
You are a senior ETF market analyst.

Your job is to explain the recommendation produced by a
multi-agent ETF analysis system.

TECHNICAL ANALYSIS

{technical}

SENTIMENT ANALYSIS

Sentiment: {sentiment["sentiment"]}
Confidence: {sentiment["confidence"]}

RISK ANALYSIS

Risk: {risk["risk"]}
Confidence: {risk["confidence"]}

FINAL DECISION

{decision["action"]}

REQUIREMENTS

1. Use ONLY the information supplied above.
2. Do not invent facts.
3. Explain how the technical signal influenced the decision.
4. Explain how news sentiment influenced the decision.
5. Explain how the risk assessment influenced the decision.
6. Discuss both positive and negative factors.
7. Provide a detailed analyst-style explanation.
8. Target approximately 250-400 words.
9. Do not provide financial guarantees.
10. Do not mention prompts, instructions,
    models, agents, or implementation details.
11. Ensure the explanation fully supports
    the final decision.

Return ONLY valid JSON:

{{
    "explanation": "...",
    "consistency": true
}}
"""

    # =====================================================
    # SECOND PASS VERIFICATION GUARDRAIL
    # =====================================================

    def _build_verification_prompt(
        self,
        technical,
        sentiment,
        risk,
        decision,
        explanation
    ):

        return f"""
You are a validation agent.

Technical Analysis:
{technical}

Sentiment:
{sentiment}

Risk:
{risk}

Decision:
{decision}

Explanation:
{explanation}

Verify whether:

1. The explanation accurately reflects
   the technical analysis.
2. The explanation accurately reflects
   the sentiment analysis.
3. The explanation accurately reflects
   the risk assessment.
4. The explanation supports the final decision.
5. The explanation introduces no new facts.
6. The explanation contains no contradictions.

Return ONLY valid JSON:

{{
    "valid": true,
    "reason": "short explanation"
}}
"""

    # =====================================================
    # LLM CALL
    # =====================================================

    def _call_llm(self, prompt):

        return self.gemini.generate(prompt)

    # =====================================================
    # VERIFICATION
    # =====================================================

    def _verify_explanation(
        self,
        technical,
        sentiment,
        risk,
        decision,
        explanation
    ):

        verification_prompt = (
            self._build_verification_prompt(
                technical,
                sentiment,
                risk,
                decision,
                explanation
            )
        )

        response = self._call_llm(
            verification_prompt
        )

        response = response.strip()

        if response.startswith("```json"):
            response = response.replace(
                "```json",
                "",
                1
            )

        if response.endswith("```"):
            response = response[:-3]

        result = json.loads(response)

        return result.get("valid", False)

    # =====================================================
    # VALIDATION GUARDRAILS
    # =====================================================

    def _validate_output(
        self,
        result,
        technical,
        sentiment,
        risk,
        decision
    ):

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

        if (
            len(explanation.strip())
            < self.MIN_EXPLANATION_LENGTH
        ):
            raise ValueError(
                "Explanation is too short."
            )

        explanation_lower = explanation.lower()

        for term in self.FORBIDDEN_TERMS:

            if term in explanation_lower:
                raise ValueError(
                    f"Guardrail violation: {term}"
                )

        action = str(
            decision["action"]
        ).upper()

        if action == "BUY":

            forbidden = [
                "recommend selling",
                "sell recommendation",
                "should sell"
            ]

            for phrase in forbidden:

                if phrase in explanation_lower:
                    raise ValueError(
                        "Explanation contradicts BUY signal."
                    )

        elif action == "SELL":

            forbidden = [
                "recommend buying",
                "buy recommendation",
                "should buy"
            ]

            for phrase in forbidden:

                if phrase in explanation_lower:
                    raise ValueError(
                        "Explanation contradicts SELL signal."
                    )

        if (
            sentiment["sentiment"].lower()
            not in explanation_lower
        ):
            raise ValueError(
                "Sentiment signal missing."
            )

        if (
            risk["risk"].lower()
            not in explanation_lower
        ):
            raise ValueError(
                "Risk signal missing."
            )

    # =====================================================
    # MAIN ENTRY POINT
    # =====================================================

    def analyze(
        self,
        technical,
        sentiment,
        risk,
        decision
    ):

        try:

            prompt = self._build_prompt(
                technical,
                sentiment,
                risk,
                decision
            )

            response = self._call_llm(
                prompt
            )

            response = response.strip()

            if response.startswith("```json"):
                response = response.replace(
                    "```json",
                    "",
                    1
                )

            if response.endswith("```"):
                response = response[:-3]

            result = json.loads(response)

            self._validate_output(
                result,
                technical,
                sentiment,
                risk,
                decision
            )

            verification_passed = (
                self._verify_explanation(
                    technical,
                    sentiment,
                    risk,
                    decision,
                    result["explanation"]
                )
            )

            if not verification_passed:

                raise ValueError(
                    "Verification guardrail failed."
                )

            return result

        except Exception as e:

            error_text = str(e)

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):
                return {
                    "explanation": (
                        "LLM quota exhausted. "
                        "Fallback explanation generated "
                        "from available agent outputs."
                    ),
                    "consistency": False,
                    "error": error_text
                }