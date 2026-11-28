"""Historic MAS backtest over collected QQQ price data.

Walks data/QQQ.csv day by day, builds Technical + price-based
Sentiment/Risk signals, decides BUY/HOLD/SELL, then runs the
Backtester and writes CSV/PNG outputs under data/.
"""

from pathlib import Path

import pandas as pd

from agents.decision_agent import DecisionAgent
from agents.technical_agent import TechnicalAgent
from backend.backtest import Backtester
from backend.metrics import compute_all_metrics
from backend.price_signals import risk_from_price, sentiment_from_price

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRICE_CSV = ROOT / "data" / "QQQ.csv"
DEFAULT_DATA_DIR = ROOT / "data"

# Technical agent needs a 30-day long MA before signals are meaningful.
MIN_HISTORY_DAYS = 30


def load_price_history(price_csv=None):
    path = Path(price_csv) if price_csv else DEFAULT_PRICE_CSV
    df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    if "Close" not in df.columns:
        raise ValueError(f"Price file missing Close column: {path}")
    return df.sort_index()


def load_news_history(news_csv):
    """Optional CSV with columns: Date, article."""
    path = Path(news_csv)
    if not path.exists():
        return {}

    news_df = pd.read_csv(path, parse_dates=["Date"])
    if "article" not in news_df.columns:
        raise ValueError("News history CSV must include an 'article' column.")

    mapping = {}
    for _, row in news_df.iterrows():
        mapping[pd.Timestamp(row["Date"]).normalize()] = str(row["article"])
    return mapping


def generate_daily_decisions(price_df, news_by_date=None, use_llm_news=False):
    """Produce one decision dict per trading day using historic prices.

    Default mode (design-spec backtest): no LLM. Sentiment/Risk come from
    price rules. If use_llm_news=True and news exists for a day, that day's
    article is passed through ETFPipeline (consumes Gemini quota).
    """
    tech_agent = TechnicalAgent()
    decision_agent = DecisionAgent()
    news_by_date = news_by_date or {}
    decisions = []
    pipeline = None

    if use_llm_news:
        from backend.etf_pipeline import ETFPipeline
        pipeline = ETFPipeline()

    for i, date in enumerate(price_df.index):
        daily_df = price_df.iloc[: i + 1]

        if len(daily_df) < MIN_HISTORY_DAYS:
            decisions.append(
                {
                    "action": 0,
                    "action_label": "HOLD",
                    "reasoning": "Warm-up: insufficient history for 30-day MA.",
                }
            )
            continue

        article = news_by_date.get(pd.Timestamp(date).normalize())

        if use_llm_news and article and pipeline is not None:
            result = pipeline.run(daily_df, article)
            decisions.append(result["decision"])
            continue

        technical = tech_agent.analyze(daily_df)
        sentiment = sentiment_from_price(daily_df)
        risk = risk_from_price(daily_df)
        decisions.append(
            decision_agent.decide(technical, sentiment, risk)
        )

    return decisions


def run_historic_backtest(
    price_csv=None,
    news_csv=None,
    use_llm_news=False,
    data_dir=None,
    save_outputs=True,
):
    """Run full historic backtest and optionally persist artifacts."""
    data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    price_df = load_price_history(price_csv)
    news_by_date = load_news_history(news_csv) if news_csv else {}

    decisions = generate_daily_decisions(
        price_df,
        news_by_date=news_by_date,
        use_llm_news=use_llm_news,
    )

    backtest_output = Backtester(price_df, decisions).run()
    equity = backtest_output["equity_curve"]
    returns = backtest_output["returns"]
    metrics = compute_all_metrics(equity, returns)

    if save_outputs:
        data_dir.mkdir(parents=True, exist_ok=True)
        equity.to_csv(data_dir / "equity_curve.csv")
        returns.to_csv(data_dir / "returns.csv")
        pd.DataFrame(decisions, index=price_df.index).to_csv(
            data_dir / "decisions.csv"
        )

    return {
        "price_df": price_df,
        "decisions": decisions,
        "backtest": backtest_output,
        "metrics": metrics,
    }
