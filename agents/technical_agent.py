import yfinance as yf
import pandas as pd

class TechnicalAgent:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
        self.summary_data = {}

    def fetch_history(self, period="1y"):
        self.data = yf.download(self.ticker, period=period)
        return self.data is not None

    def compute_indicators(self):
        close = self.data["Close"]

        sma20 = close.rolling(20).mean().iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1]

        # Convert Series → float safely
        if hasattr(sma20, "iloc"):
            sma20 = float(sma20.iloc[0])
        else:
            sma20 = float(sma20)

        if hasattr(sma50, "iloc"):
            sma50 = float(sma50.iloc[0])
        else:
            sma50 = float(sma50)

        # Now signal is ALWAYS defined
        if sma20 > sma50:
            signal = "BUY"
        elif sma20 < sma50:
            signal = "SELL"
        else:
            signal = "HOLD"

        self.summary_data = {
            "sma20": sma20,
            "sma50": sma50,
            "signal": signal
        }



    def summary(self):
        if not self.summary_data:
            self.compute_indicators()

        return self.summary_data

    
    def moving_averages(self):
        close = self.data["Close"]

        return {
            "MA20": float(close.rolling(20).mean().dropna().iloc[-1]),
            "MA50": float(close.rolling(50).mean().dropna().iloc[-1]),
            "MA200": float(close.rolling(200).mean().dropna().iloc[-1])
        }



    def rsi(self, period=14):
        close = self.data["Close"]
        delta = close.diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1]

    def macd(self):
        close = self.data["Close"]

        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        return {
            "MACD": macd.iloc[-1],
            "Signal": signal.iloc[-1]
        }

    def mean_reversion(self, window=20):
        close = self.data["Close"]

        mean = close.rolling(window).mean()
        std = close.rolling(window).std()

        zscore = (close - mean) / std

        return zscore.dropna().iloc[-1]
