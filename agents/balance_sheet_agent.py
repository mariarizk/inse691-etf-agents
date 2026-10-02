import yfinance as yf
import numpy as np

class BalanceSheetAgent:
    def __init__(self, ratio_thresholds):
        self.thresholds = ratio_thresholds

    def get_value(self, bs, keys):
        for key in keys:
            if key in bs.index:
                return bs.loc[key].iloc[0]
        return None

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

    def analyze_company(self, ticker):
        try:
            bs = yf.Ticker(ticker).balance_sheet

            total_assets = self.get_value(bs, ["Total Assets"])
            total_liabilities = self.get_value(bs, ["Total Liabilities Net Minority Interest", "Total Liab"])
            shareholder_equity = self.get_value(bs, ["Total Stockholder Equity", "Stockholders Equity"])

            current_assets = self.get_value(bs, ["Current Assets", "Total Current Assets"])
            current_liabilities = self.get_value(bs, ["Current Liabilities", "Total Current Liabilities"])

            cash = self.get_value(bs, ["Cash And Cash Equivalents", "Cash"])
            short_term_investments = self.get_value(bs, ["Short Term Investments"])

            long_term_debt = self.get_value(bs, ["Long Term Debt"])
            short_term_debt = self.get_value(bs, ["Short Term Debt", "Short Long Term Debt"])

            # Fix NoneType math
            long_term_debt = long_term_debt or 0
            short_term_debt = short_term_debt or 0
            total_debt = long_term_debt + short_term_debt

            # Ratios (safe division)
            current_ratio = self.safe_div(current_assets, current_liabilities)
            quick_ratio = self.safe_div((cash or 0) + (short_term_investments or 0), current_liabilities)
            debt_to_equity = self.safe_div(total_debt, shareholder_equity)
            debt_ratio = self.safe_div(total_liabilities, total_assets)
            cash_ratio = self.safe_div(cash, current_liabilities)

            # Scores
            liquidity_score = self.score_ratio(current_ratio, self.thresholds["current_ratio"])
            debt_score = self.score_ratio(debt_to_equity, self.thresholds["debt_to_equity"])
            cash_score = self.score_ratio(cash_ratio, self.thresholds["cash_ratio"])

            balance_sheet_score = np.mean([liquidity_score, debt_score, cash_score])

            return {
                "current_ratio": current_ratio,
                "quick_ratio": quick_ratio,
                "debt_to_equity": debt_to_equity,
                "debt_ratio": debt_ratio,
                "cash_ratio": cash_ratio,
                "liquidity_score": liquidity_score,
                "debt_score": debt_score,
                "cash_score": cash_score,
                "balance_sheet_score": balance_sheet_score
            }

        except Exception as e:
            return {"error": str(e), "balance_sheet_score": 1}
