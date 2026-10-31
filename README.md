# Multi‑Agent System (MAS) for QQQ ETF Trading

This project implements a simple, interpretable Multi‑Agent System (MAS) that analyzes the QQQ ETF and generates daily BUY, HOLD, or SELL signals. The system is designed for academic use and demonstrates how multiple lightweight agents can collaborate to form a trading decision.

The MAS processes historical QQQ price data, produces daily signals, runs a full backtest, and generates performance plots such as equity curve, drawdown, rolling volatility, rolling Sharpe ratio, and a comparison against QQQ buy‑and‑hold. An LLM layer then reads the latest news, moderates conflicting signals, explains the final decision (checked by a hallucination guard), and writes a plain‑language performance report. Every agent message is recorded in an agent communication log.

---

## 🏗️ Architecture

```
QQQ prices ──► Technical / Sentiment / Risk agents ──► Blackboard ──► Decision Agent ──► Backtester
                                                       ▲   │   │                              │
Marketaux news ──► News Sentiment Agent (LLM) ─────────┘   │   └──► data/agent_log.json       ▼
                                                           ▼                          Report Agent (LLM)
                                               Debate Agent (LLM) ──► Explanation Agent (LLM)
                                                                          │       ▲
                                                                          ▼       │ retry once
                                                                     Consistency Guard
```

The full diagram is in [`docs/architecture.drawio`](docs/architecture.drawio) (open it with [draw.io](https://app.diagrams.net)). All LLM prompts, inputs, outputs and fallbacks are documented in [`docs/prompt_templates.md`](docs/prompt_templates.md).

Rule‑based agents drive the daily backtest, so results are deterministic. LLM agents run once per analysis and never inside the backtest loop. If the LLM is unavailable, the rule‑based decision is kept.

---

## 🧠 Agents Overview

### Rule‑based agents

| Agent | Input | Output |
|---|---|---|
| **TechnicalAgent** | 10 / 30‑day moving‑average crossover | bullish, neutral, bearish |
| **SentimentAgent** | latest daily return | positive, neutral, negative |
| **RiskAgent** | 20‑day volatility | low, medium, high |
| **Blackboard** | outputs of every agent | shared memory for agent‑to‑agent communication |
| **DecisionAgent** | signals read from the blackboard | `1` BUY, `0` HOLD, `-1` SELL |

Thresholds for every agent live in `config.py` (`AGENT_CONFIG`).

### LLM agents (`agents/llm/`)

| Agent | Role |
|---|---|
| **NewsSentimentAgent** | Scores the tone of the latest QQQ headlines from Marketaux as positive, neutral or negative. |
| **DebateAgent** | Moderator. Runs only when agents conflict (e.g. bullish trend but negative sentiment, negative news or high risk), weighs the bull and bear case, and sets the final action. |
| **ExplanationAgent** | Justifies the final BUY / HOLD / SELL decision in plain language. |
| **ReportAgent** | Explains backtest results (total return, CAGR, Sharpe ratio, max drawdown) against QQQ buy‑and‑hold. |

The LLM is Google Gemini through its OpenAI‑compatible endpoint (free tier). Any OpenAI‑compatible provider works by changing `LLM_BASE_URL` and `LLM_MODEL`.

### Safeguards and logging

- **Consistency guard** (`agents/llm/consistency_guard.py`): a rule‑based hallucination check. The explanation must state the final action, must not recommend a different one, and must not describe an agent with the opposite of its signal. On failure the explanation is regenerated once; if it still fails it is flagged.
- **Agent communication log**: every blackboard write is recorded with step, sender, timestamp and content. `scripts/run_llm_report.py` saves it to `data/agent_log.json`, `GET /analysis` returns it, and the dashboard shows it.

---

## ⚙️ Setup

### 1. Create a virtual environment and install dependencies
Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create a `.env` file in the project root
```bash
GEMINI_API_KEY=your_gemini_key          # https://aistudio.google.com/apikey
MARKETAUX_API_KEY=your_marketaux_key    # news for the News Sentiment Agent
EODHD_API_KEY=your_eodhd_key            # only needed to refresh data/QQQ.csv
FMP_API_KEY=your_fmp_key
# Optional overrides
LLM_MODEL=gemini-3.5-flash-lite
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
```
`.env` is ignored by git. Never commit API keys.

---

## ▶️ How to Run the Project

```bash
# Run the MAS pipeline
python scripts/run_pipeline.py

# Run the backtest
python scripts/run_backtest.py

# Generate plots
python scripts/plot_equity.py
python scripts/plot_drawdown.py
python scripts/plot_returns_histogram.py
python scripts/plot_rolling_metrics.py
python scripts/compare_vs_buyhold.py

# LLM decision explanation + backtest report (saves data/llm_report.md and data/agent_log.json)
python scripts/run_llm_report.py

# API (GET /analysis, GET /backtest)
uvicorn backend.api:app --reload

# Dashboard
streamlit run frontend/dashboard.py

# Tests
python -m unittest discover tests
```
