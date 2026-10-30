import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from backend.advisor import Advisor
from backend.strategy import load_prices
from config import DATA_DIR

price_df = load_prices()
advisor = Advisor()

analysis = advisor.analyze_latest(price_df)
backtest = advisor.backtest_report(price_df)
final = analysis["final_decision"]

report = "\n".join([
    f"# QQQ MAS Report ({analysis['date']})",
    "",
    f"## Decision: {final['label']} (decided by {final['source']})",
    "",
    analysis["explanation"],
    "",
    "## Agent signals",
    "",
    "```json",
    json.dumps(analysis["signals"], indent=2),
    "```",
    "",
    "## Debate",
    "",
    json.dumps(final["debate"], indent=2) if final["debate"] else (final["note"] or "No conflict between agents."),
    "",
    "## Backtest performance",
    "",
    backtest["report"],
    "",
    "```json",
    json.dumps({"mas_strategy": backtest["strategy_metrics"],
                "qqq_buy_and_hold": backtest["benchmark_metrics"]}, indent=2),
    "```",
    "",
])

(DATA_DIR / "llm_report.md").write_text(report, encoding="utf-8")
print(report)
print("Saved data/llm_report.md")
