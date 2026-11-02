# Multi‑Agent System (MAS) for QQQ ETF Trading

This project implements an interpretable Multi‑Agent System (MAS) of **five agents** that analyzes the QQQ ETF and generates daily BUY, HOLD, or SELL signals. The system is designed for academic use and demonstrates how a small set of agents, some rule‑based and some LLM‑based, collaborate through a shared blackboard to form a trading decision.

The MAS processes historical QQQ price data, produces daily signals, runs a full backtest, and generates performance plots such as equity curve, drawdown, rolling volatility, rolling Sharpe ratio, and a comparison against QQQ buy‑and‑hold. For the latest trading day it also reads financial news with an LLM and explains the decision in plain language. Every agent message is recorded in an agent communication log.

---

## 🏗️ Architecture

```
QQQ prices ─────┬──► Technical Agent (rules) ──┐
                │                              ▼
Marketaux news ─┼──► Sentiment Agent (LLM) ──► Blackboard ──► Decision Agent ──► Backtester
                │                              ▲    │              │
                └──► Risk Agent (LLM) ─────────┘    │              ▼
                                                    │      Explanation Agent (LLM)
                                                    └──► data/agent_log.json
```

The full diagram is in [`docs/architecture.drawio`](docs/architecture.drawio) (open it with [draw.io](https://app.diagrams.net)). All LLM prompts, inputs, outputs and fallbacks are documented in [`docs/prompt_templates.md`](docs/prompt_templates.md).

- **Backtest:** there is no historical news, so the Sentiment and Risk agents use their price‑based rules (latest daily return, 20‑day volatility) and the Explanation agent is skipped. Results are deterministic and need no LLM calls.
- **Live analysis:** fetches the latest QQQ headlines and runs all five agents with the LLM.

---

## 🧠 Agents Overview

| Agent | Type | Input | Output |
|---|---|---|---|
| **TechnicalAgent** | Rule‑based | 10 / 30‑day moving‑average crossover | `bullish`, `neutral`, `bearish` |
| **SentimentAgent** | LLM (price fallback) | financial news (or latest daily return) | `Positive` / `Neutral` / `Negative`, confidence 0–100, reasoning |
| **RiskAgent** | LLM (price fallback) | financial news + 20‑day volatility (or volatility alone) | `Low` / `Medium` / `High`, confidence 0–100, reasoning |
| **DecisionAgent** | Rule‑based | signals read from the blackboard; LLM outputs below 60 confidence are ignored | `1` BUY, `0` HOLD, `-1` SELL, reasoning |
| **ExplanationAgent** | LLM | all agent outputs on the blackboard | plain‑language justification of the decision |

The **Blackboard** (`agents/blackboard.py`) is the shared memory the agents use to communicate; it is not an agent. Thresholds live in `config.py` (`AGENT_CONFIG`).

The LLM is Google Gemini through its OpenAI‑compatible endpoint (free tier). OpenAI or any other OpenAI‑compatible provider works by setting `LLM_BASE_URL`, `LLM_MODEL` and `LLM_API_KEY`.

### Safeguards and logging

- **Fallbacks:** if there is no news or the LLM fails, the Sentiment and Risk agents return their price‑based result, so the system always produces a decision.
- **Consistency check:** the Explanation agent checks its own text against the decision and agent signals (it must state the final action, must not recommend another one, and must not contradict an agent's signal). On failure it regenerates once; if it still fails the explanation is flagged.
- **Agent communication log:** every blackboard write is recorded with step, sender, timestamp and content. `scripts/run_analysis.py` saves it to `data/agent_log.json`, `GET /analysis` returns it, and the dashboard shows it.

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
MARKETAUX_API_KEY=your_marketaux_key    # news for the Sentiment and Risk agents
EODHD_API_KEY=your_eodhd_key            # only needed to refresh data/QQQ.csv
FMP_API_KEY=your_fmp_key
# Optional: use OpenAI or another OpenAI-compatible provider instead of Gemini
LLM_API_KEY=your_key
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

# Live five-agent analysis with news + LLM (saves data/analysis.md and data/agent_log.json)
python scripts/run_analysis.py

# API (GET /analysis, GET /backtest)
uvicorn backend.api:app --reload

# Dashboard
streamlit run frontend/dashboard.py

# Tests
python -m unittest discover tests
```
