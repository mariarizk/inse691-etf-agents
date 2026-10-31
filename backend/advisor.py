import math

from agents.llm.client import LlmClient
from agents.llm.debate_agent import DebateAgent
from agents.llm.explanation_agent import ExplanationAgent
from agents.llm.news_sentiment_agent import NewsSentimentAgent
from agents.llm.report_agent import ReportAgent
from agents.llm.signals import context_signals
from backend.etf_pipeline import ETFPipeline
from backend.metrics import compute_all_metrics
from backend.strategy import buy_and_hold, run_strategy
from backend.utils.news_downloader import fetch_headlines
from config import TICKER


def _clean_metrics(metrics):
    return {
        name: None if math.isnan(value) else round(float(value), 4)
        for name, value in metrics.items()
    }


class Advisor:
    """LLM layer on top of the rule-based agents: news, debate, explanation and report."""

    def __init__(self, client=None):
        client = client or LlmClient()
        self.news_agent = NewsSentimentAgent(client)
        self.debate_agent = DebateAgent(client)
        self.explanation_agent = ExplanationAgent(client)
        self.report_agent = ReportAgent(client)

    def analyze_latest(self, price_df):
        pipeline = ETFPipeline(price_df)
        pipeline.run()
        board = pipeline.blackboard

        board.write(self.news_agent.name, self.news_agent.analyze(fetch_headlines(TICKER)))

        final_decision = self.debate_agent.moderate(board.all())
        board.write(self.debate_agent.name, final_decision)

        explanation = self.explanation_agent.explain(board.all(), final_decision)
        board.write(self.explanation_agent.name, explanation)

        return {
            "date": price_df.index[-1].date().isoformat(),
            "signals": context_signals(board.all()),
            "rule_decision": board.read("decision"),
            "final_decision": final_decision,
            "explanation": explanation,
            "log": board.history(),
        }

    def backtest_report(self, price_df):
        _, strategy = run_strategy(price_df)
        benchmark = buy_and_hold(price_df)

        strategy_metrics = _clean_metrics(
            compute_all_metrics(strategy["equity_curve"], strategy["returns"])
        )
        benchmark_metrics = _clean_metrics(
            compute_all_metrics(benchmark["equity_curve"], benchmark["returns"])
        )

        return {
            "strategy_metrics": strategy_metrics,
            "benchmark_metrics": benchmark_metrics,
            "report": self.report_agent.write(strategy_metrics, benchmark_metrics),
        }
