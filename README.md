# QQQ Multi-Agent ETF Intelligence System

Working prototype for **INSE 691 – Foundations of AI Agent Systems** (Fall 2026).

A multi-agent system analyzes the QQQ ETF and produces **BUY / HOLD / SELL** recommendations using Technical, Sentiment, Risk, Decision, and Explanation/Conversation agents, with prompt-injection guardrails, blackboard memory, agent logs, a web dashboard, and historic backtesting.

| Field | Value |
|---|---|
| Course | INSE 691 – Foundations of AI Agent Systems |
| Students | Aneri Rangani (40312334), Maria Rizk (40020692) |
| Ticker in scope | QQQ only |

Also see:
- [Architecture enhancements summary](docs/Architecture_Changes.md)
- [Testing and Evaluation Report](docs/INSE691_Testing_and_Evaluation_Report.md) (also submitted as a Word document)

---

## What is included

- `agents/` — Technical, Sentiment, Risk, Decision, Explanation, Conversation, Blackboard
- `backend/` — ETF pipeline, Gemini client, guardrails, historic backtest, FastAPI app
- `templates/` + `static/` — web dashboard
- `data/QQQ.csv` — collected historic QQQ closes (2025-10-02 → 2026-10-01)
- `tests/` — automated unit / integration / guardrail / backtest cases
- `scripts/` — backtest, metrics, and plot generators

---

## Requirements

- Python **3.10+**
- Internet for `pip install` and live Gemini calls
- A Gemini API key in `.env` for **live news analysis** (historic backtest and most unit tests work **without** a key)

---

## Setup

Extract the ZIP and open a terminal in the extracted folder.

**macOS / Linux**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# edit .env and set GEMINI_API_KEY=your_key
```

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
# edit .env and set GEMINI_API_KEY=your_key
```

---

## Run the working prototype (web dashboard)

```sh
uvicorn backend.api:app --reload --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Try three outcomes

1. **Normal analysis.** Paste a financial news article (≥ 20 characters) and click **Analyze News**. The dashboard shows Technical, Sentiment, Risk, Decision, and Explanation outputs.
2. **Guardrail block.** Paste text containing `ignore previous instructions` or a very short string. Input validation / injection defense should reject or fall back safely.
3. **Conversation follow-up.** After a successful analysis, ask a follow-up (for example: “Why was the decision BUY?”). The Conversation Agent retrieves blackboard memory and answers from stored analysis only.

Useful pages: `/` dashboard, `/agents`, `/logs`, `/agent-logs`, `/backtest`, `/health`.

---

## Historic backtest (collected data, no LLM)

Uses `data/QQQ.csv`. Sentiment/Risk use price rules so the run is reproducible and does not consume Gemini quota.

```sh
python scripts/run_backtest.py
python scripts/compute_metrics.py
python scripts/compare_vs_buyhold.py
python scripts/plot_equity.py
python scripts/plot_drawdown.py
python scripts/plot_rolling_metrics.py
python scripts/plot_returns_histogram.py
```

Outputs are written under `data/` (CSV + PNG). The `/backtest` page displays the saved plots.

Optional LLM-on-news days (quota limited):

```sh
python scripts/run_backtest.py --news data/news_history.csv --llm-news
```

`news_history.csv` must have columns `Date,article`.

---

## Run automated tests

From the project root:

```sh
python -m unittest discover -s tests -v
```

Expected: all tests **OK** (offline suite does not require Gemini).

---

## Notes

- Gemini free-tier quota is limited (roughly a small number of live LLM calls per day). Prefer the offline backtest and unit tests for bulk evaluation; reserve live LLM calls for the demo.
- Do not commit real API keys. Use `.env` locally only.
