import pandas as pd

from backend.backtest import Backtester
from backend.etf_pipeline import ETFPipeline
from config import PRICE_FILE


def load_prices(path=PRICE_FILE):
    return pd.read_csv(path, parse_dates=["Date"], index_col="Date")


def generate_decisions(price_df):
    """Runs the pipeline once per day using only the data available up to that day."""
    return [ETFPipeline(price_df.loc[:date]).run()["decision"] for date in price_df.index]


def run_strategy(price_df):
    decisions = generate_decisions(price_df)
    return decisions, Backtester(price_df, decisions).run()


def buy_and_hold(price_df):
    returns = price_df["Close"].pct_change().fillna(0)
    return {"returns": returns, "equity_curve": (1 + returns).cumprod()}
