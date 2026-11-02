from fastapi import FastAPI

from backend.strategy import analyze_latest, backtest_metrics, load_prices

app = FastAPI(title="QQQ Multi-Agent Trading System")


@app.get("/analysis")
def latest_analysis():
    return analyze_latest(load_prices())


@app.get("/backtest")
def backtest():
    return backtest_metrics(load_prices())
