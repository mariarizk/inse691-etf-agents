import yfinance as yf
import pandas as pd
import numpy as np

class RiskAgent:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def fetch_history(self, period="1y"):
        try:
            self.data = yf.download(self.ticker, period=period)
            return True
        except Exception as e:
            print("Error fetching history:", e)
            return False

    def volatility(self):
        if self.data is None:
            return None
        
        returns = self.data["Close"].pct_change(fill_method=None)
        return returns.std() * np.sqrt(252)

    def max_drawdown(self):
        if self.data is None:
            return None

        close = self.data["Close"]
        rolling_max = close.cummax()
        drawdown = (close - rolling_max) / rolling_max
        return drawdown.min()

    def leverage_decay(self):
        if self.ticker not in ["TQQQ", "SQQQ"]:
            return None

        returns = self.data["Close"].pct_change()
        decay = (returns.std() ** 2) * 3  # leverage factor
        return decay

    def risk_score(self):
        vol = self.volatility()
        dd = self.max_drawdown()

        # Convert Series → float
        if hasattr(vol, "iloc"):
            vol = vol.iloc[0]
        if hasattr(dd, "iloc"):
            dd = dd.iloc[0]

        score = 0

        # Volatility scoring
        if vol > 0.25:
            score += 2
        elif vol > 0.15:
            score += 1

        # Drawdown scoring
        if dd < -0.20:
            score += 2
        elif dd < -0.10:
            score += 1

        return score
    s
    def summary(self):
        # Ensure data is loaded
        if self.data is None:
            self.fetch_history()

        return {
            "volatility": self.volatility(),
            "max_drawdown": self.max_drawdown(),
            "leverage_decay": self.leverage_decay(),
            "risk_score": self.risk_score()
        }
