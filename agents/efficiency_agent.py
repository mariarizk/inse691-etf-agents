import yfinance as yf
import numpy as np

class EfficiencyAgent:
    def __init__(self, ratio_thresholds):
        """
        ratio_thresholds example:
        {
            "roe": {"good": 0.15, "neutral": 0.08},
            "roa": {"good": 0.08, "neutral": 0.04},
            "asset_turnover": {"good": 0.7, "neutral": 0.3}
        }
        """
        self.thresholds = ratio_thresholds

    def safe_div(self, a, b):
        if a is None or b in (None, 0):
            return None
        return a / b

    def score_ratio(self, value, thresholds):
        if value is None or np.isnan(value):
            return 1
        if value >= thresholds["good"]:
            return 3
        elif value >= thresholds["neutral"]:
            return 2
        return 1

    def get_value(self, df, keys):
        for key in keys:
            if key in df.index:
                return df.loc[key].iloc[0]
        return None

    def analyze_company(self, ticker):
        try:
            t = yf.Ticker(ticker)
            inc = t.financials
            bs = t.balance_sheet

            net_income = self.get_value(inc, ["Net Income"])
            revenue = self.get_value(inc, ["Total Revenue", "Revenue"])

            total_assets = self.get_value(bs, ["Total Assets"])
            equity = self.get_value(bs, ["Total Stockholder Equity", "Stockholders Equity"])

            roa = self.safe_div(net_income, total_assets)
            roe = self.safe_div(net_income, equity)
            asset_turnover = self.safe_div(revenue, total_assets)

            roa_score = self.score_ratio(roa, self.thresholds["roa"])
            roe_score = self.score_ratio(roe, self.thresholds["roe"])
            asset_turnover_score = self.score_ratio(asset_turnover, self.thresholds["asset_turnover"])

            efficiency_score = np.mean([roa_score, roe_score, asset_turnover_score])

            return {
                "roa": roa,
                "roe": roe,
                "asset_turnover": asset_turnover,
                "roa_score": roa_score,
                "roe_score": roe_score,
                "asset_turnover_score": asset_turnover_score,
                "efficiency_score": efficiency_score
            }

        except Exception as e:
            return {"error": str(e), "efficiency_score": 1}
