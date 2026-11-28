# Note for Maria

Hi Maria — quick handoff from **Aneri Rangani (40312334)**.

## What I did (after your final Git push)

I took ownership of testing + evaluation through the Dec 1 submission window, as we discussed:

1. **Pulled your latest `main`** (autonomous agents, website, guardrails, agent logs).
2. **Fixed historic backtest / scripts** so they work with the current `ETFPipeline` API (they were still on the old constructor).
3. **Added** `backend/historic_backtest.py` + `backend/price_signals.py` so we can backtest on collected `data/QQQ.csv` without burning Gemini quota.
4. **Reworked the automated tests** (37 tests, all passing) — agents, guardrails, conversation memory, pipeline, API pages, backtest.
5. **Ran evaluation** and wrote the **Testing and Evaluation Report**.
6. **Built the Moodle submission packages** under `../Submission/`.

## What you can proofread (as you offered)

- `docs/INSE691_Testing_and_Evaluation_Report.docx` (also `.md`)
- `README.md` run instructions
- Optional: `docs/NOTE_FOR_MARIA.md` (this file)

I am **not** asking you to do more coding on this. A proofread pass before we submit the report is perfect.

## How to pull my updates

```bash
git checkout main
git pull origin main
```

Then open:

- `docs/INSE691_Testing_and_Evaluation_Report.docx`
- `README.md`

## Submission files (local folder)

`/Users/yashmehta/INSE 691/Submission/`

- `QQQ-Multi-Agent-ETF-Working-Prototype.zip` → Working Prototype assignment  
- `INSE691_Testing_and_Evaluation_Report.docx` → Testing and Evaluation Report assignment  

## Quick verify

```bash
python -m unittest discover -s tests -v
uvicorn backend.api:app --reload --host 127.0.0.1 --port 8000
```

Thanks again for finishing the implementation and the architecture-changes / run doc — that made testing straightforward.

— Aneri
