# LLM Prompt Templates

All prompts live in [`agents/llm/prompts.py`](../agents/llm/prompts.py). Every LLM call goes through `LlmClient` ([`agents/llm/client.py`](../agents/llm/client.py)), which uses Google Gemini through its OpenAI‑compatible endpoint (`temperature = 0.2`, up to 2 retries on HTTP 429/500/503). Settings are in `LLM_CONFIG` in [`config.py`](../config.py).

LLM agents run once per analysis (latest trading day) and once per backtest report. They never run inside the daily backtest loop, so backtest results stay deterministic.

| Order | Agent | Prompt | Output | Runs when |
|---|---|---|---|---|
| 1 | News Sentiment Agent | `NEWS_SENTIMENT_SYSTEM` | JSON | headlines were fetched from Marketaux |
| 2 | Debate Agent | `DEBATE_SYSTEM` | JSON | agent signals conflict |
| 3 | Explanation Agent | `EXPLANATION_SYSTEM`, `EXPLANATION_RETRY` | text | every analysis |
| 4 | Report Agent | `REPORT_SYSTEM` | text | every backtest report |

---

## 1. News Sentiment Agent

**File:** [`agents/llm/news_sentiment_agent.py`](../agents/llm/news_sentiment_agent.py)

**Role:** score the tone of the latest QQQ headlines.

**Input (user message):** JSON list of up to 3 headlines from [`backend/utils/news_downloader.py`](../backend/utils/news_downloader.py):

```json
[{"title": "...", "description": "...", "source": "...", "published_at": "..."}]
```

**System prompt:**

```text
You are the news sentiment analyst in a multi-agent trading system for the
QQQ ETF (Nasdaq-100).

Read the headlines and summaries provided and judge their overall tone for QQQ over the next few
trading days.

Reply with JSON only, using exactly these keys:
{"signal": "positive" or "neutral" or "negative", "score": number from -1 to 1, "summary": "..."}

Keep the summary under 40 words. Use only the headlines provided.
```

**Validation:** `signal` must be one of positive / neutral / negative; `score` is clamped to [-1, 1].

**Fallback:** no headlines, an LLM error or an invalid reply gives `signal = "neutral"`, `score = 0` and a `note` explaining why.

---

## 2. Debate Agent (moderator)

**File:** [`agents/llm/debate_agent.py`](../agents/llm/debate_agent.py)

**Role:** settle the final action when agents disagree.

**When it runs:** only if at least one agent is bullish (technical `bullish`, sentiment or news `positive`) and at least one is bearish (technical `bearish`, sentiment or news `negative`, risk `high`). Otherwise the rule‑based decision is final and no LLM call is made.

**Input (user message):**

```text
Agent outputs:
{"technical": {...}, "sentiment": {...}, "risk": {...}, "news_sentiment": {...}}

Rule-based decision: SELL
```

**System prompt:**

```text
You are the debate moderator in a multi-agent trading system for the QQQ ETF.
The technical, sentiment and risk agents (and the news sentiment agent, when present) disagree.
Weigh the bullish case against the bearish case and choose one final action.

Reply with JSON only, using exactly these keys:
{"bull_case": "...", "bear_case": "...", "verdict": "...", "action": "BUY" or "HOLD" or "SELL"}

Keep each text field under 60 words. Base your reasoning only on the agent outputs provided.
```

**Validation:** `action` must be BUY, HOLD or SELL.

**Fallback:** an LLM error or invalid action keeps the rule‑based decision (`source = "rules"`) with a `note`.

---

## 3. Explanation Agent

**File:** [`agents/llm/explanation_agent.py`](../agents/llm/explanation_agent.py)

**Role:** justify the final BUY / HOLD / SELL in plain language for a non‑expert investor.

**Input (user message):**

```json
{
  "signals": {"technical": {...}, "sentiment": {...}, "risk": {...}, "news_sentiment": {...}},
  "rule_based_decision": "SELL",
  "final_decision": "HOLD",
  "decided_by": "debate",
  "debate_verdict": "..."
}
```

**System prompt** (`{max_words}` = 120):

```text
You explain trading decisions made by a multi-agent system for the QQQ ETF
to a non-expert investor.

Justify the final action using the agent signals and numbers provided, and say which agents
supported or opposed it. If a debate moderator overruled the rule-based decision, say why.
State the final action explicitly as BUY, HOLD or SELL and describe each agent's signal exactly
as given. Write one short paragraph of at most {max_words} words. Do not invent data and do not
give personalised financial advice.
```

**Retry prompt**, appended to the input when the consistency guard fails:

```text
Your previous explanation was:
{previous}

It failed these consistency checks:
{issues}

Rewrite the explanation so that it passes every check.
```

**Consistency guard (hallucination check):** [`agents/llm/consistency_guard.py`](../agents/llm/consistency_guard.py) is rule‑based, not an LLM. It checks that the explanation:

1. states the final action (BUY / HOLD / SELL, including "buying", "holding", "selling");
2. does not recommend a different action (for example "we recommend selling" when the final action is HOLD);
3. does not describe an agent with the opposite of its signal (for example "the trend is bearish" when the technical agent is bullish, or "volatility is high" when risk is low).

The agent makes at most `explanation_max_attempts = 2` attempts (one regeneration). If the second attempt still fails, the explanation is returned with `consistent = false` and the list of `issues`, and the dashboard shows a warning.

**Fallback:** an LLM error returns `"Explanation unavailable: ..."` with `consistent = null`.

---

## 4. Report Agent

**File:** [`agents/llm/report_agent.py`](../agents/llm/report_agent.py)

**Role:** explain backtest performance against QQQ buy‑and‑hold.

**Input (user message):** metrics from [`backend/metrics.py`](../backend/metrics.py):

```json
{
  "mas_strategy": {"Total Return": 0.0, "CAGR": 0.0, "Volatility": 0.0, "Sharpe Ratio": 0.0, "Max Drawdown": 0.0, "Calmar Ratio": 0.0, "...": 0.0},
  "qqq_buy_and_hold": {"...": 0.0}
}
```

**System prompt** (`{max_words}` = 250):

```text
You write plain-language performance reports for a multi-agent trading strategy
on the QQQ ETF.

Compare the strategy with QQQ buy-and-hold using only the metrics provided (total return, CAGR,
volatility, Sharpe ratio, maximum drawdown, Calmar ratio). Explain what each number means for an
investor, state which approach did better on return and which on risk, and finish with one
limitation of this backtest. Use at most {max_words} words.
```

**Fallback:** an LLM error returns `"Report unavailable: ..."`.

---

## Agent communication log

Every agent result is written to the `Blackboard` ([`agents/blackboard.py`](../agents/blackboard.py)), which also appends a log entry:

```json
{"step": 1, "sender": "technical", "timestamp": "2026-10-30T23:59:00+00:00", "content": {...}}
```

The order for one analysis is technical, sentiment, risk, decision, news_sentiment, debate, explanation. `python scripts/run_llm_report.py` saves the log to `data/agent_log.json`; the API returns it under `log` from `GET /analysis`, and the dashboard shows it as a table.
