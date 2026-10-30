import json

from agents.llm.client import LlmError
from agents.llm.prompts import REPORT_SYSTEM
from config import LLM_CONFIG


class ReportAgent:
    """Turns backtest metrics into a plain-language performance report."""

    name = "report"

    def __init__(self, client, max_words=LLM_CONFIG["report_max_words"]):
        self.client = client
        self.system_prompt = REPORT_SYSTEM.format(max_words=max_words)

    def write(self, strategy_metrics, benchmark_metrics):
        payload = {
            "mas_strategy": strategy_metrics,
            "qqq_buy_and_hold": benchmark_metrics,
        }

        try:
            return self.client.complete(self.system_prompt, json.dumps(payload, indent=2))
        except LlmError as exc:
            return f"Report unavailable: {exc}"
