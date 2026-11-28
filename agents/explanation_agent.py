import json
import time

from backend.gemini_client import GeminiClient
from backend.agentlogger import AgentLogger


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

    AVAILABLE_TOOLS = [
        "generate_explanation",
        "fallback_explanation"
    ]

    def __init__(self):

        self.gemini = GeminiClient()

    # =====================================================
    # TOOL SELECTION
    # =====================================================

    def _select_tool(
        self,
        technical,
        sentiment,
        risk,
        decision
    ):

        prompt = f"""
You are an Explanation Agent.

Available tools:

1. generate_explanation
   - Detailed explanation generation.

2. fallback_explanation
   - Simple deterministic explanation.

Technical:
{technical}

Sentiment:
{sentiment}

Risk:
{risk}

Decision:
{decision}

Return ONLY valid JSON:

{{
    "tool":"generate_explanation"
}}
"""

        if not self.gemini.available:
            return "fallback_explanation"

        try:

            response = self.gemini.generate(
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

            tool = result.get(
                "tool",
                "generate_explanation"
            )

            if tool not in self.AVAILABLE_TOOLS:

                return "generate_explanation"

            return tool

        except Exception:

            return "fallback_explanation"

    # =====================================================
    # EXPLANATION TOOL
    # =====================================================

    def _build_generation_prompt(
        self,
        technical,
        sentiment,
        risk,
        decision
    ):

        return f"""
You are a senior ETF market analyst.

Your job is to explain the recommendation
produced by a multi-agent ETF analysis system.

TECHNICAL ANALYSIS

{technical}

SENTIMENT ANALYSIS

Sentiment: {sentiment["sentiment"]}
Confidence: {sentiment["confidence"]}

RISK ANALYSIS

Risk: {risk["risk"]}
Confidence: {risk["confidence"]}

FINAL DECISION

{decision["action_label"]}

REQUIREMENTS

1. Use ONLY the information supplied above.
2. Never invent facts.
3. Explain how technical signals
   influenced the recommendation.
4. Explain how sentiment influenced
   the recommendation.
5. Explain how risk influenced
   the recommendation.
6. Discuss both supporting and
   opposing signals.
7. Generate a detailed explanation.
8. Target 250-400 words.
9. Do not provide guarantees.
10. Do not mention prompts,
    instructions,
    models,
    hidden messages,
    system messages,
    agents,
    or implementation details.
11. Ensure consistency with the
    recommendation.

Return ONLY valid JSON:

{{
    "explanation": "...",
    "consistency": true
}}
"""

    # =====================================================
    # FALLBACK TOOL
    # =====================================================

    def _fallback_explanation_tool(
        self,
        technical,
        sentiment,
        risk,
        decision
    ):

        return {
            "tool_used":
                "fallback_explanation",
            "explanation": (
                f"The system produced a "
                f"{decision['action_label']} "
                f"recommendation based on the "
                f"combined assessment of technical "
                f"signals, market sentiment, and "
                f"investment risk."
            ),
            "consistency": False
        }

    # =====================================================
    # VERIFY EXPLANATION
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

Sentiment Analysis:

{sentiment}

Risk Analysis:

{risk}

Decision:

{decision}

Explanation:

{explanation}

Verify whether:

1. The explanation reflects
   technical analysis.
2. The explanation reflects
   sentiment analysis.
3. The explanation reflects
   risk analysis.
4. The explanation supports
   the final recommendation.
5. No facts were invented.
6. No contradictions exist.

Return ONLY valid JSON:

{{
    "valid": true,
    "reason": "verification summary"
}}
"""

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

        response = self.gemini.generate(
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

        result = json.loads(
            response
        )

        return result.get(
            "valid",
            False
        )

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

        explanation = result[
            "explanation"
        ]

        if not isinstance(
            explanation,
            str
        ):
            raise ValueError(
                "Explanation must be a string."
            )

        if (
            len(explanation.strip())
            < self.MIN_EXPLANATION_LENGTH
        ):
            raise ValueError(
                "Explanation too short."
            )

        explanation_lower = (
            explanation.lower()
        )

        for term in (
            self.FORBIDDEN_TERMS
        ):

            if term in (
                explanation_lower
            ):

                raise ValueError(
                    f"Guardrail violation: {term}"
                )

        if (
            sentiment["sentiment"].lower()
            not in explanation_lower
        ):
            raise ValueError(
                "Sentiment not referenced."
            )

        if (
            risk["risk"].lower()
            not in explanation_lower
        ):
            raise ValueError(
                "Risk not referenced."
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

        start_time = time.time()

        try:

            selected_tool = (
                self._select_tool(
                    technical,
                    sentiment,
                    risk,
                    decision
                )
            )

            if (
                selected_tool
                == "fallback_explanation"
            ):

                result = (
                    self._fallback_explanation_tool(
                        technical,
                        sentiment,
                        risk,
                        decision
                    )
                )

            else:

                prompt = (
                    self._build_generation_prompt(
                        technical,
                        sentiment,
                        risk,
                        decision
                    )
                )

                response = (
                    self.gemini.generate(
                        prompt
                    )
                )

                response = response.strip()

                if response.startswith(
                    "```json"
                ):
                    response = response.replace(
                        "```json",
                        "",
                        1
                    )

                if response.endswith(
                    "```"
                ):
                    response = response[:-3]

                result = json.loads(
                    response
                )

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

                result["tool_used"] = (
                    "generate_explanation"
                )

            execution_time = round(
                (
                    time.time()
                    - start_time
                ) * 1000
            )

            AgentLogger.log(
                agent="ExplanationAgent",
                tool_used=result["tool_used"],
                status="success",
                execution_time_ms=execution_time,
                metadata={
                    "consistency":
                        result[
                            "consistency"
                        ],
                    "decision":
                        decision[
                            "action_label"
                        ]
                }
            )

            return result

        except Exception as e:

            execution_time = round(
                (
                    time.time()
                    - start_time
                ) * 1000
            )

            error_text = str(e)

            AgentLogger.log(
                agent="ExplanationAgent",
                tool_used="fallback_explanation",
                status="fallback",
                execution_time_ms=execution_time,
                metadata={
                    "error":
                        error_text[:200]
                }
            )

            return {
                "tool_used":
                    "fallback_explanation",
                "explanation": (
                    f"The system produced a "
                    f"{decision['action_label']} "
                    f"recommendation based on the "
                    f"combined assessment of technical "
                    f"signals, market sentiment, and "
                    f"investment risk. A detailed "
                    f"explanation could not be generated "
                    f"or verified, so a fallback "
                    f"explanation was provided."
                ),
                "consistency": False,
                "error": error_text
            }