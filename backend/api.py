from fastapi import FastAPI

from backend.advisor import Advisor
from backend.strategy import load_prices

app = FastAPI(title="QQQ Multi-Agent Trading System")
advisor = Advisor()


@app.get("/analysis")
def latest_analysis():
    return advisor.analyze_latest(load_prices())


@app.get("/backtest")
def backtest_report():
    return advisor.backtest_report(load_prices())
