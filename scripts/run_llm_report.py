import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from backend.advisor import Advisor
from backend.strategy import load_prices
from config import AGENT_LOG_FILE, DATA_DIR

price_df = load_prices()
advisor = Advisor()

analysis = advisor.analyze_latest(price_df)
backtest = advisor.backtest_report(price_df)
final = analysis["final_decision"]
explanation = analysis["explanation"]

if explanation["consistent"] is None:
    guard_result = "Not checked (LLM unavailable)."
elif explanation["consistent"]:
    guard_result = f"Passed after {explanation['attempts']} attempt(s)."
else:
    guard_result = "Flagged: " + " ".join(explanation["issues"])

report = "\n".join([
    f"# QQQ MAS Report ({analysis['date']})",
    "",
    f"## Decision: {final['label']} (rule-based: {analysis['rule_decision']['label']}, decided by {final['source']})",
    "",
    explanation["text"],
    "",
    f"Consistency guard: {guard_result}",
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
AGENT_LOG_FILE.write_text(json.dumps(analysis["log"], indent=2, default=str), encoding="utf-8")

print(report)
print("Saved data/llm_report.md and data/agent_log.json")
