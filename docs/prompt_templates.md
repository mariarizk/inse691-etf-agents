# LLM Prompt Templates

Three of the five agents use an LLM: **Sentiment**, **Risk** and **Explanation**. The Technical and Decision agents are rule‑based.

Every LLM call goes through `LlmClient` ([`agents/llm_client.py`](../agents/llm_client.py)), which uses Google Gemini through its OpenAI‑compatible endpoint by default (`temperature = 0.2`, up to 2 retries on HTTP 429/500/503). Settings are in `LLM_CONFIG` in [`config.py`](../config.py); OpenAI works by setting `LLM_BASE_URL`, `LLM_MODEL` and `LLM_API_KEY`.

The LLM agents run only in the live analysis of the latest trading day. In the backtest there is no news, so Sentiment and Risk use their price‑based rules and the Explanation agent is skipped.

| Agent | Prompt location | Output | Fallback |
|---|---|---|---|
| Sentiment | `SentimentAgent._build_prompt` | JSON | latest daily return rule |
| Risk | `RiskAgent._build_prompt` | JSON | 20‑day volatility rule |
| Explanation | `SYSTEM_PROMPT`, `RETRY_PROMPT` in `explanation_agent.py` | text | "Explanation unavailable" |

The news text given to Sentiment and Risk is built by `headlines_to_text` in [`backend/utils/news_downloader.py`](../backend/utils/news_downloader.py) from up to 3 Marketaux headlines (title, description, source, date).

---

## 1. Sentiment Agent

**File:** [`agents/sentiment_agent.py`](../agents/sentiment_agent.py)

**System prompt:** `You are a financial sentiment analyst. Reply with valid JSON only.`

**User prompt:**

```text
You are a financial sentiment analyst.

Analyze the following financial news article.

Classify sentiment as exactly one of:

- Positive
- Neutral
- Negative

Return ONLY valid JSON, with confidence as a number from 0 to 100:

{
    "sentiment": "...",
    "confidence": 0,
    "reasoning": "..."
}

Article:
{article_text}
```

**Validation:** `sentiment` must be Positive, Neutral or Negative; `confidence` is clamped to 0–100.

**Fallback:** no news, an LLM error or an invalid reply gives the price‑based result (Positive above +1% daily return, Negative below −1%, otherwise Neutral) with `source = "price"`.

---

## 2. Risk Agent

**File:** [`agents/risk_agent.py`](../agents/risk_agent.py)

**System prompt:** `You are a financial risk analyst. Reply with valid JSON only.`

**User prompt:**

```text
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

Current 20-day volatility of QQQ daily returns: {volatility}

Return ONLY valid JSON, with confidence as a number from 0 to 100:

{
    "risk": "...",
    "confidence": 0,
    "reasoning": "..."
}

Article:
{article_text}
```

**Validation:** `risk` must be Low, Medium or High; `confidence` is clamped to 0–100.

**Fallback:** the volatility rule (Low below 1%, Medium below 2%, otherwise High) with `source = "price"`.

---

## 3. Explanation Agent

**File:** [`agents/explanation_agent.py`](../agents/explanation_agent.py)

**Input (user message):** the technical, sentiment, risk and decision outputs from the blackboard as JSON.

**System prompt** (`{max_words}` = 120):

```text
You explain trading decisions made by a multi-agent system for the QQQ ETF
to a non-expert investor.

Justify the final action using the agent outputs provided, and say which agents supported or
opposed it. State the final action explicitly as BUY, HOLD or SELL and describe each agent's
signal exactly as given. Write one short paragraph of at most {max_words} words. Do not invent
data and do not give personalised financial advice.
```

**Retry prompt**, appended when the consistency check fails:

```text
Your previous explanation was:
{previous}

It failed these consistency checks:
{issues}

Rewrite the explanation so that it passes every check.
```

**Consistency check** (`check_consistency`, rule‑based): the explanation must

1. state the final action (BUY / HOLD / SELL, including "buying", "holding", "selling");
2. not recommend a different action;
3. not describe an agent with the opposite of its signal (for example "the trend is bearish" when the technical agent is bullish, or "volatility is high" when risk is Low).

At most `explanation_max_attempts = 2` attempts are made. If the second still fails, the explanation is returned with `consistent = false` and the list of `issues`.

---

## Decision rules (not an LLM)

The Decision agent ignores Sentiment and Risk outputs whose confidence is below 60, then:

- **SELL** if technical is bearish, sentiment is Negative, or risk is High;
- **BUY** if technical is bullish, sentiment is Positive, and risk is Low;
- **HOLD** otherwise.

## Agent communication log

Every agent result is written to the `Blackboard` ([`agents/blackboard.py`](../agents/blackboard.py)), which appends a log entry:

```json
{"step": 1, "sender": "technical", "timestamp": "2026-11-01T23:59:00+00:00", "content": {...}}
```

The order for one analysis is technical, sentiment, risk, decision, explanation. `python scripts/run_analysis.py` saves the log to `data/agent_log.json`; `GET /analysis` returns it under `log`, and the dashboard shows it as a table.
