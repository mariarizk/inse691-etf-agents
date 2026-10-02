import yfinance as yf
import numpy as np

class CashFlowAgent:
    def __init__(self, ratio_thresholds):
        """
        ratio_thresholds example:
        {
            "cash_flow_margin": {"good": 0.20, "neutral": 0.10},
            "fcf_margin": {"good": 0.10, "neutral": 0.00},
            "ocf_growth": {"good": 0.10, "neutral": 0.00}
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

    def get_prev_value(self, df, keys):
        for key in keys:
            if key in df.index and len(df.loc[key]) > 1:
                return df.loc[key].iloc[1]
        return None

    def analyze_company(self, ticker):
        try:
            cf = yf.Ticker(ticker).cashflow
            inc = yf.Ticker(ticker).financials

            # Cash flow fields
            operating_cf = self.get_value(cf, ["Operating Cash Flow"])
            prev_operating_cf = self.get_prev_value(cf, ["Operating Cash Flow"])

            capex = self.get_value(cf, ["Capital Expenditure"])
            free_cf = operating_cf - abs(capex or 0) if operating_cf is not None else None

            prev_capex = self.get_prev_value(cf, ["Capital Expenditure"])
            prev_free_cf = (
                prev_operating_cf - abs(prev_capex or 0)
                if prev_operating_cf is not None
                else None
            )

            # Revenue for margins
            revenue = self.get_value(inc, ["Total Revenue", "Revenue"])

            # Ratios
            cash_flow_margin = self.safe_div(operating_cf, revenue)
            fcf_margin = self.safe_div(free_cf, revenue)

            ocf_growth = self.safe_div(operating_cf - prev_operating_cf, prev_operating_cf)
            fcf_growth = self.safe_div(free_cf - prev_free_cf, prev_free_cf)

            # Scores
            cash_strength_score = self.score_ratio(cash_flow_margin, self.thresholds["cash_flow_margin"])
            fcf_score = self.score_ratio(fcf_margin, self.thresholds["fcf_margin"])
            growth_score = self.score_ratio(ocf_growth, self.thresholds["ocf_growth"])

            cashflow_score = np.mean([cash_strength_score, fcf_score, growth_score])

            return {
                "cash_flow_margin": cash_flow_margin,
                "fcf_margin": fcf_margin,
                "ocf_growth": ocf_growth,
                "fcf_growth": fcf_growth,
                "cash_strength_score": cash_strength_score,
                "fcf_score": fcf_score,
                "growth_score": growth_score,
                "cashflow_score": cashflow_score
            }

        except Exception as e:
            return {"error": str(e), "cashflow_score": 1}
