import math

import pandas as pd

from agents.llm_client import LlmClient
from backend.backtest import Backtester
from backend.etf_pipeline import ETFPipeline
from backend.metrics import compute_all_metrics
from backend.utils.news_downloader import fetch_headlines, headlines_to_text
from config import PRICE_FILE, TICKER


def load_prices(path=PRICE_FILE):
    return pd.read_csv(path, parse_dates=["Date"], index_col="Date")


def generate_decisions(price_df):
    """Runs the pipeline once per day on data up to that day; no news or LLM, so results are deterministic."""
    pipeline = ETFPipeline()
    return [pipeline.run(price_df.loc[:date])["decision"] for date in price_df.index]


def run_strategy(price_df):
    decisions = generate_decisions(price_df)
    return decisions, Backtester(price_df, decisions).run()


def buy_and_hold(price_df):
    returns = price_df["Close"].pct_change().fillna(0)
    return {"returns": returns, "equity_curve": (1 + returns).cumprod()}


def analyze_latest(price_df):
    """Live run of all five agents on the latest day, using today's QQQ headlines and the LLM."""
    headlines = fetch_headlines(TICKER)
    result = ETFPipeline(LlmClient()).run(price_df, headlines_to_text(headlines), explain=True)
    return {"date": price_df.index[-1].date().isoformat(), "headlines": headlines, **result}


def _clean_metrics(metrics):
    return {
        name: None if math.isnan(value) else round(float(value), 4)
        for name, value in metrics.items()
    }


def backtest_metrics(price_df):
    _, strategy = run_strategy(price_df)
    benchmark = buy_and_hold(price_df)
    return {
        "strategy_metrics": _clean_metrics(compute_all_metrics(strategy["equity_curve"], strategy["returns"])),
        "benchmark_metrics": _clean_metrics(compute_all_metrics(benchmark["equity_curve"], benchmark["returns"])),
    }
