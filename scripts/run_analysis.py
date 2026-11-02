import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from backend.strategy import analyze_latest, backtest_metrics, load_prices
from config import AGENT_LOG_FILE, ANALYSIS_FILE

price_df = load_prices()
analysis = analyze_latest(price_df)
backtest = backtest_metrics(price_df)

decision = analysis["decision"]
explanation = analysis.get("explanation") or {"text": "", "consistent": None, "issues": [], "attempts": 0}

if explanation["consistent"] is None:
    check_result = "Not checked (LLM unavailable)."
elif explanation["consistent"]:
    check_result = f"Passed after {explanation['attempts']} attempt(s)."
else:
    check_result = "Flagged: " + " ".join(explanation["issues"])

headlines = [f"- {h['title']} ({h['source']})" for h in analysis["headlines"]] or ["- No headlines available."]

report = "\n".join([
    f"# QQQ MAS Analysis ({analysis['date']})",
    "",
    f"## Decision: {decision['label']}",
    "",
    decision["reasoning"],
    "",
    "## Explanation",
    "",
    explanation["text"],
    "",
    f"Consistency check: {check_result}",
    "",
    "## Agent signals",
    "",
    "```json",
    json.dumps({name: analysis[name] for name in ("technical", "sentiment", "risk")}, indent=2),
    "```",
    "",
    "## News analysed",
    "",
    *headlines,
    "",
    "## Backtest metrics",
    "",
    "```json",
    json.dumps({"mas_strategy": backtest["strategy_metrics"],
                "qqq_buy_and_hold": backtest["benchmark_metrics"]}, indent=2),
    "```",
    "",
])

ANALYSIS_FILE.write_text(report, encoding="utf-8")
AGENT_LOG_FILE.write_text(json.dumps(analysis["log"], indent=2, default=str), encoding="utf-8")

print(report)
print("Saved data/analysis.md and data/agent_log.json")
