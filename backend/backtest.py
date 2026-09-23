import pandas as pd
import numpy as np
from backend.pipeline import ETFPipeline
import matplotlib.pyplot as plt
import os

class Backtester:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.results = []

    def load_data(self):
        import yfinance as yf
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        data = data[['Close']]
        data.dropna(inplace=True)
        return data

    def run(self):
        data = self.load_data()

        for date in data.index:
            # Rolling window slice up to current date
            window_data = data.loc[:date]

            # Run full pipeline
            pipeline = ETFPipeline(self.ticker)
            output = pipeline.run()

            # Store results
            self.results.append({
                "date": date,
                "close": window_data.iloc[-1]['Close'],
                "decision": output["decision"]["decision"],
                "confidence": output["decision"]["confidence"],
                "risk_score": output["risk"]["risk_score"],
                "bullish": len(output["debate"]["bullish_arguments"]),
                "bearish": len(output["debate"]["bearish_arguments"]),
                "conflicts": len(output["debate"]["conflicts"])
            })

        return pd.DataFrame(self.results)
    
    def compute_performance(self, df):
        # Initialize position
        position = 0
        positions = []

        for decision in df['decision']:
            if decision == 'BUY':
                position = 1
            elif decision == 'SELL':
                position = 0
            # HOLD keeps the current position
            positions.append(position)

        df['position'] = positions

        # Strategy return = market return * position
        df['strategy_return'] = df['return'] * df['position']


    def plot_results(self, df):
        plt.figure(figsize=(12,6))
        plt.plot(df['equity_curve'], label='Strategy Equity Curve')
        plt.title(f"{self.ticker} Strategy Backtest")
        plt.legend()

        # SAVE EQUITY CURVE HERE
        plt.savefig(f"data/equity_curve_{self.ticker}.png")

        plt.show()

        plt.figure(figsize=(12,4))
        plt.plot(df['drawdown'], label='Drawdown', color='red')
        plt.title("Drawdown")
        plt.legend()

        # SAVE DRAWDOWN HERE
        plt.savefig(f"data/drawdown_{self.ticker}.png")

        plt.show()


    def save_results(self, df):
        path = os.path.join("data", f"backtest_{self.ticker}.csv")
        df.to_csv(path, index=False)
        print(f"Saved backtest results to {path}")
