# INSE 691 — Testing and Evaluation Report

**Multi-Agent LLM-Driven System for QQQ Analysis and Risk-Aware Decision Support**

| Field | Value |
|---|---|
| Course | INSE 691 Foundations of AI Agent Systems, Fall 2026 |
| Institution | Concordia University, Gina Cody School of Engineering and Computer Science |
| Students | Aneri Rangani (40312334), Maria Rizk (40020692) |
| Prototype | QQQ Multi-Agent ETF Intelligence System |
| Report date | 27 November 2026 |
| Submission | Testing and Evaluation Report (due 48 hours before booked presentation) |
| Authorship note | **Aneri Rangani** completed the testing suite updates, historic backtest on collected QQQ data, evaluation metrics/plots, this Testing and Evaluation Report, and the working-prototype submission package after Maria’s final implementation push. |

---

## 1. Introduction

This report documents testing and evaluation of the QQQ multi-agent prototype. The coding implementation of the autonomous agents, dashboard, guardrails, and logging was finalized and pushed by **Maria Rizk**. The testing, historic backtest evaluation, report writing, and submission packaging described here were completed by **Aneri Rangani (40312334)**. It covers (1) test and evaluation cases for important components and functionalities, (2) procedures to run those cases, and (3) observed results. Testing combines automated unit/integration tests, guardrail checks, end-to-end pipeline checks, API page checks, and a historic backtest on collected QQQ price data.

The system under test includes:

- Technical Agent (moving-average trend)
- Sentiment Agent (LLM / rule-based news sentiment)
- Risk Agent (LLM / rule-based news risk)
- Decision Agent (BUY / HOLD / SELL rules + confidence gate)
- Explanation / Conversation Agents (explanation, memory, retrieval tools)
- Guardrails (empty/short input, prompt-injection patterns)
- Blackboard + AgentLogger observability
- Historic backtester and performance metrics
- FastAPI web dashboard

---

## 2. Testing and Evaluation Cases

### 2.1 Component unit cases

| ID | Component | Case | Expected result |
|---|---|---|---|
| T1 | Technical Agent | Rising price series (40 days) | Label `bullish` |
| T2 | Technical Agent | Falling price series (40 days) | Label `bearish` |
| T3 | Technical Agent | Real `data/QQQ.csv` slice | Label in {bullish, bearish, neutral} |
| T4 | Decision Agent | bullish + Positive(≥60) + Low(≥60) | action `1` / BUY |
| T5 | Decision Agent | bearish technical | action `-1` / SELL |
| T6 | Decision Agent | Positive sentiment with confidence 40 | Forced Neutral → HOLD |
| T7 | Decision Agent | Invalid technical label | `ValueError` |
| T8 | Sentiment Agent | Positive earnings article | Valid label + confidence 0–100 + reasoning |
| T9 | Sentiment Agent | Rule-based path on growth keywords | `Positive` |
| T10 | Risk Agent | Litigation / regulatory article | Valid Low/Medium/High structure |
| T11 | Risk Agent | Rule-based “lawsuit” text | `High` |
| T12 | Explanation Agent | BUY decision inputs | Explanation length > 20; consistency bool present |

### 2.2 Guardrail cases

| ID | Case | Expected result |
|---|---|---|
| G1 | Empty article → Sentiment / Risk | `ValueError` |
| G2 | Short article `"QQQ"` → Sentiment / Risk | `ValueError` |
| G3 | `validate_article` with “ignore previous instructions…” | `ValueError` (injection) |
| G4 | Conversation input containing jailbreak phrases | `ValueError` |
| G5 | Conversation chat with no prior analysis | `ValueError` |

### 2.3 Conversation / memory / tools

| ID | Case | Expected result |
|---|---|---|
| C1 | `store_analysis` then read session state | Article + analysis stored |
| C2 | `retrieve_decision` tool | Returns stored BUY decision |
| C3 | `chat` with mocked Gemini | Response mentions BUY; history length 1 |

### 2.4 Pipeline and system integration

| ID | Case | Expected result |
|---|---|---|
| P1 | `ETFPipeline.run(QQQ.csv, valid article)` offline | Keys: technical, sentiment, risk, decision, explanation; blackboard has `pipeline_result` |
| P2 | Sentiment agent forced to raise | Pipeline fallback Neutral sentiment; run continues |
| P3 | Full system: live pipeline + historic backtest | Decision action in {-1,0,1}; equity curve length = price length |

### 2.5 Backtest / evaluation cases

| ID | Case | Expected result |
|---|---|---|
| B1 | `Backtester` with constant BUY | positions/returns/equity lengths match price history |
| B2 | Price-based sentiment/risk helpers | Labels in allowed sets; `source=price` |
| B3 | Historic walk on `data/QQQ.csv` | One decision per day; warm-up HOLD for first 29 days |
| B4 | Persist outputs | `equity_curve.csv`, `returns.csv`, `decisions.csv` written |
| B5 | Metrics vs buy-and-hold plots | Metrics printable; PNGs generated under `data/` |

### 2.6 API / dashboard cases

| ID | Case | Expected result |
|---|---|---|
| A1 | `GET /` | HTTP 200 |
| A2 | `GET /backtest` | HTTP 200 |
| A3 | `GET /health` | HTTP 200 |
| A4 | `POST /analyze` with short article | HTTP 200 (error rendered safely in page) |

### 2.7 Manual evaluation scenarios (live demo)

| ID | Scenario | Purpose |
|---|---|---|
| M1 | Paste constructive earnings article | End-to-end LLM/rule path + BUY/HOLD/SELL |
| M2 | Paste injection string | Guardrail rejection / safe handling |
| M3 | Ask follow-up after analysis | Conversation retrieval + answer from memory |
| M4 | Open `/agent-logs` and `/logs` | Observability of tools and blackboard |
| M5 | Open `/backtest` after scripts | Equity / drawdown / Sharpe / vs buy-hold charts |

---

## 3. Procedures for Running the Testing and Evaluation Cases

### 3.1 Environment setup

```sh
cd QQQ-Multi-Agent-ETF-Ready   # extracted prototype folder
python3 -m venv .venv
source .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env           # optional for live LLM cases M1–M3
```

Working directory must be the project root so `data/QQQ.csv` resolves correctly.

### 3.2 Automated suite (covers T*, G*, C*, P*, B1–B4, A*)

```sh
python -m unittest discover -s tests -v
```

Mapping:

- `tests/test_technical_agent.py` → T1–T3  
- `tests/test_decision_agent.py` → T4–T7  
- `tests/test_sentiment_agent.py` → T8–T9  
- `tests/test_risk_agent.py` → T10–T11  
- `tests/test_explanation_agent.py` → T12  
- `tests/test_guardrails.py` → G1–G5  
- `tests/test_conversation_agent.py` → C1–C3  
- `tests/test_etf_pipeline.py` → P1–P2  
- `tests/test_full_system.py` → P3  
- `tests/test_backtest.py` → B1–B4  
- `tests/test_api.py` → A1–A4  

### 3.3 Historic backtest evaluation (B3–B5)

```sh
python scripts/run_backtest.py
python scripts/compute_metrics.py
python scripts/compare_vs_buyhold.py
python scripts/plot_equity.py
python scripts/plot_drawdown.py
python scripts/plot_rolling_metrics.py
python scripts/plot_returns_histogram.py
```

This walks every trading day in `data/QQQ.csv`, applies Technical + price-based Sentiment/Risk + Decision (no Gemini), then computes strategy returns and equity.

### 3.4 Manual live evaluation (M1–M5)

```sh
uvicorn backend.api:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 and execute scenarios M1–M5. Note: Gemini quota may limit the number of live LLM calls per day; rule-based fallbacks still allow the demo to continue.

---

## 4. Testing and Evaluation Results

### 4.1 Automated unit / integration results

Executed on 27 November 2026 from the project root:

```text
python -m unittest discover -s tests -v
Ran 37 tests in 0.231s
OK
```

| Suite | Tests | Result |
|---|---:|---|
| Technical Agent | 3 | PASS |
| Decision Agent | 4 | PASS |
| Sentiment Agent | 2 | PASS |
| Risk Agent | 2 | PASS |
| Explanation Agent | 1 | PASS |
| Guardrails | 7 | PASS |
| Conversation Agent | 3 | PASS |
| ETF Pipeline | 5 | PASS |
| Full system | 1 | PASS |
| Backtest / price signals / historic | 5 | PASS |
| API pages | 4 | PASS |
| **Total** | **37** | **All PASS** |

### 4.2 Guardrail results (summary)

- Empty and short articles are rejected before LLM use (G1–G2).  
- Prompt-injection phrases are blocked by `validate_article` and Conversation input validation (G3–G4).  
- Conversation refuses chat until an analysis is stored (G5).  
- Pipeline wraps Sentiment failures with Neutral fallback so Decision still runs (P2).

### 4.3 Historic backtest evaluation results

**Data:** `data/QQQ.csv` — 251 trading days (2025-10-02 to 2026-10-01).  
**Mode:** design-spec historic mode (price rules, no live news LLM calls).  
**Warm-up:** first 29 days forced HOLD (30-day MA not ready).

| Metric | Value |
|---|---:|
| Total Return | -16.91% |
| CAGR | -16.96% |
| Volatility (ann.) | 14.94% |
| Sharpe Ratio | -1.30 |
| Max Drawdown | -18.50% |
| Calmar Ratio | -0.92 |
| Mean Daily Return | -0.069% |
| Std Daily Return | 0.941% |

| Decision label | Count |
|---|---:|
| HOLD | 125 |
| SELL | 120 |
| BUY | 6 |

**Interpretation.** On this collected window the rule-based MAS is conservative (few BUY days, many SELL/HOLD). Absolute return underperforms a simple long-only QQQ path over the same sample. This is acceptable for an academic decision-support prototype: the evaluation goal is to verify that agents produce auditable, guardrailed decisions and that the backtest pipeline is reproducible—not to claim trading alpha.

Artifacts generated for evaluation visuals: `data/equity_curve.png`, `data/drawdown.png`, `data/rolling_sharpe.png`, `data/rolling_volatility.png`, `data/returns_histogram.png`, `data/mas_vs_buyhold.png`, plus CSV decision/return/equity files.

### 4.4 Weaknesses and residual risks identified during testing

1. **Gemini quota / latency** — Live LLM paths are quota-limited; tool selection itself may call Gemini, so demos should cache a few articles and rely on fallbacks.  
2. **Backtest without news** — Historic mode uses price proxies for Sentiment/Risk; it does not prove LLM news quality over history unless a `news_history.csv` + `--llm-news` run is added (quota costly).  
3. **SELL-heavy rule set** — Any bearish technical **or** Negative sentiment **or** High risk triggers SELL; this biases the strategy defensive and can miss upside.  
4. **Legacy Streamlit frontend** — `frontend/dashboard.py` still references an older class name; the supported UI is the FastAPI templates app.  
5. **Warm-up days** — First ~30 days are HOLD-only by design; metrics include that period.  
6. **Conversation depends on prior analyze** — Follow-ups without a stored analysis correctly fail; UX should guide users to analyze first.

### 4.5 Evaluation conclusions

| Objective | Status |
|---|---|
| Important agents covered by automated cases | Met (37/37 PASS) |
| Guardrails exercised | Met (empty/short/injection/no-memory) |
| Procedures documented and runnable | Met |
| Historic evaluation on collected data | Met (metrics + plots) |
| Web prototype pages load | Met (API tests PASS) |
| Known limitations recorded | Met (Section 4.4) |

The prototype is suitable for course demonstration and submission: core agent behaviours, guardrails, observability, and reproducible historic evaluation are verified. Live LLM quality should be shown with a small number of curated articles during the presentation.

---

## 5. How this maps to the submission checklist

1. **Testing and evaluation cases covering important components and functionalities** — Section 2 (T/G/C/P/B/A/M).  
2. **Procedures of running the testing and evaluation cases** — Section 3.  
3. **Testing and evaluation results** — Section 4.

---

## Appendix A — Command quick reference

```sh
python -m unittest discover -s tests -v
python scripts/run_backtest.py
uvicorn backend.api:app --reload --host 127.0.0.1 --port 8000
```

## Appendix B — Repository / package layout (prototype ZIP)

```text
agents/  backend/  data/  docs/  scripts/  static/  templates/  tests/
README.md  requirements.txt  .env.example  config.py
```
