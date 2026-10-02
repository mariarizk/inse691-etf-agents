from fastapi import FastAPI
from backend.etf_pipeline import ETFPipeline
from config import CONFIG

app = FastAPI()
system = ETFMultiAgentSystem(CONFIG)

@app.get("/run/{ticker}")
def run_ticker(ticker: str):
    return system.run(ticker)

@app.get("/run_many")
def run_many(tickers: str):
    tickers_list = tickers.split(",")
    return system.run_many(tickers_list)
