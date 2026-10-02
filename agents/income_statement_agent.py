import yfinance as yf
import numpy as np

class IncomeStatementAgent:
    def __init__(self, ratio_thresholds):
        """
        ratio_thresholds example:
        {
            "net_margin": {"good": 0.15, "neutral": 0.05},
            "revenue_growth": {"good": 0.10, "neutral": 0.00},
            "eps": {"good": 0.0, "neutral": -0.1}
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
            inc = yf.Ticker(ticker).financials

            revenue = self.get_value(inc, ["Total Revenue", "Revenue"])
            gross_profit = self.get_value(inc, ["Gross Profit"])
            operating_income = self.get_value(inc, ["Operating Income"])
            net_income = self.get_value(inc, ["Net Income"])

            prev_revenue = self.get_prev_value(inc, ["Total Revenue", "Revenue"])
            prev_net_income = self.get_prev_value(inc, ["Net Income"])

            basic_eps = self.get_value(inc, ["Basic EPS"])
            diluted_eps = self.get_value(inc, ["Diluted EPS"])
            eps = diluted_eps or basic_eps

            # Ratios
            gross_margin = self.safe_div(gross_profit, revenue)
            operating_margin = self.safe_div(operating_income, revenue)
            net_margin = self.safe_div(net_income, revenue)

            revenue_growth = self.safe_div(revenue - prev_revenue, prev_revenue)
            net_income_growth = self.safe_div(net_income - prev_net_income, prev_net_income)

            # Scores
            profitability_score = self.score_ratio(net_margin, self.thresholds["net_margin"])
            growth_score = self.score_ratio(revenue_growth, self.thresholds["revenue_growth"])
            eps_score = self.score_ratio(eps, self.thresholds["eps"])

            income_statement_score = np.mean([profitability_score, growth_score, eps_score])

            return {
                "gross_margin": gross_margin,
                "operating_margin": operating_margin,
                "net_margin": net_margin,
                "revenue_growth": revenue_growth,
                "net_income_growth": net_income_growth,
                "eps": eps,
                "profitability_score": profitability_score,
                "growth_score": growth_score,
                "eps_score": eps_score,
                "income_statement_score": income_statement_score
            }

        except Exception as e:
            return {"error": str(e), "income_statement_score": 1}
