# QQQ Multi-Agent ETF Intelligence System — Architecture Enhancements

## Purpose

Summary of improvements: guardrails, autonomous tool selection, conversation memory, observability, and agent execution logging.

1. **Security Guardrails** — Prompt-injection protections on LLM agents; input validation for jailbreaks / instruction overrides; output checks that reject prompt disclosure.
2. **Conversation Agent** — Follow-up Q&A after article analysis using session memory of blackboard outputs.
3. **Autonomous retrieval tools** — Conversation Agent selects among `retrieve_sentiment`, `retrieve_risk`, `retrieve_decision`, `retrieve_explanation`, `retrieve_article`, `retrieve_full_analysis`.
4. **Sentiment tools** — Chooses `llm_sentiment_analysis` or `rule_based_sentiment_analysis`.
5. **Risk tools** — Chooses `llm_risk_analysis` or `rule_based_risk_analysis`, with fallback on API failure.
6. **Explanation improvements** — Detailed explanation, verification, deterministic fallback.
7. **Blackboard** — Shared communication for Technical, Sentiment, Risk, Decision, Explanation.
8. **AgentLogger** — Execution traces (timestamps, tools, status, timing, metadata).
9. **Agent Logs dashboard** — `/agent-logs` page for transparency.
10. **Graceful degradation** — Rate/quota limits switch agents to fallback instead of hard failure.
11. **Agentic behavior demonstrated** — Memory, tool selection, retrieval, routing, guardrails, observability, explainability.

## Run

```sh
uvicorn backend.api:app --reload
```

Open http://127.0.0.1:8000
