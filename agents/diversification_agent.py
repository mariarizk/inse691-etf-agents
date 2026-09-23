import yfinance as yf
import pandas as pd
import numpy as np

class DiversificationAgent:
    def __init__(self, tickers, meta):
        """
        tickers: list of ticker symbols
        meta: dict like {
            "QQQ": {"sector": "Tech", "leverage": 1},
            ...
        }
        """
        self.tickers = tickers
        self.meta = meta
        self.data = None

    def fetch_history(self, period="1y"):
        try:
            self.data = yf.download(self.tickers, period=period)["Close"]
            return True
        except Exception as e:
            print("Error fetching history:", e)
            return False

    def returns(self):
        if self.data is None:
            return None

        rets = self.data.pct_change(fill_method=None)
        return rets.dropna()

    def correlation_matrix(self):
        rets = self.returns()
        if rets is None or rets.empty:
            return None

        return rets.corr()

    def avg_correlation(self):
        corr = self.correlation_matrix()
        if corr is None:
            return None

        mask = ~np.eye(len(corr), dtype=bool)
        vals = corr.values[mask]
        if len(vals) == 0:
            return None

        return vals.mean()

    def correlation_score(self):
        """
        0–4 points based on average correlation.
        Lower avg correlation → higher score.
        """
        avg_corr = self.avg_correlation()
        if avg_corr is None:
            return 0

        score = 0
        if avg_corr < 0.2:
            score = 4
        elif avg_corr < 0.4:
            score = 3
        elif avg_corr < 0.7:
            score = 2
        elif avg_corr < 0.9:
            score = 1
        else:
            score = 0

        return score

    def sector_diversity_score(self):
        """
        0–3 points based on number of distinct sectors.
        More distinct sectors → higher score.
        """
        sectors = []
        for t in self.tickers:
            info = self.meta.get(t, {})
            sector = info.get("sector", None)
            if sector is not None:
                sectors.append(sector)

        unique_sectors = set(sectors)
        n = len(unique_sectors)

        if n >= 3:
            return 3
        elif n == 2:
            return 2
        elif n == 1:
            return 1
        else:
            return 0

    def leverage_penalty(self):
        """
        -3 to 0 points.
        More leveraged/inverse products → bigger penalty.
        """
        penalty = 0
        for t in self.tickers:
            info = self.meta.get(t, {})
            lev = info.get("leverage", 1)

            if abs(lev) == 3:
                penalty -= 2  # strong penalty for 3x
            elif abs(lev) > 1:
                penalty -= 1  # mild penalty for >1x

            if lev < 0:
                penalty -= 1  # extra penalty for inverse

        # cap penalty at -3
        return max(penalty, -3)

    def count_score(self):
        """
        0–2 points based on number of tickers.
        """
        n = len(self.tickers)
        if n >= 5:
            return 2
        elif n >= 3:
            return 1
        else:
            return 0

    def diversification_score(self):
        """
        Final score 0–10 combining:
        - correlation_score (0–4)
        - sector_diversity_score (0–3)
        - count_score (0–2)
        - leverage_penalty (-3–0)
        """
        corr = self.correlation_score()
        sector = self.sector_diversity_score()
        count = self.count_score()
        lev_pen = self.leverage_penalty()

        raw_score = corr + sector + count + lev_pen

        # clamp to [0, 10]
        return max(0, min(10, raw_score))

    def summary(self):
        return {
            "tickers": self.tickers,
            "avg_correlation": self.avg_correlation(),
            "correlation_score": self.correlation_score(),
            "sector_diversity_score": self.sector_diversity_score(),
            "count_score": self.count_score(),
            "leverage_penalty": self.leverage_penalty(),
            "score": self.diversification_score()

        }
