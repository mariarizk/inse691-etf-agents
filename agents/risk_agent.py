import yfinance as yf
import numpy as np
import pandas as pd

from agents.balance_sheet_agent import BalanceSheetAgent


class RiskAgent:
    def __init__(self, ratio_thresholds, balance_sheet_thresholds):
        """
        ratio_thresholds example:
        {
            "beta": {"good": 1.0, "neutral": 1.2},
            "volatility": {"good": 0.02, "neutral": 0.04},
            "drawdown": {"good": -0.10, "neutral": -0.20},
            "debt_to_equity": {"good": 1.0, "neutral": 2.0},
            "current_ratio": {"good": 1.5, "neutral": 1.0}
        }
        """
        self.thresholds = ratio_thresholds
        self.bs_agent = BalanceSheetAgent(balance_sheet_thresholds)

    def score_inverse(self, value, thresholds):
        # lower risk is better
        if value is None or np.isnan(value):
            return 1
        if value <= thresholds["good"]:
            return 3
        elif value <= thresholds["neutral"]:
            return 2
        return 1

    def safe_div(self, a, b):
        if a is None or b in (None, 0):
            return None
        return a / b

    def analyze_company(self, ticker):
        try:
            t = yf.Ticker(ticker)
            info = t.info if hasattr(t, "info") else t.get_info()

            # Market risk
            beta = info.get("beta")

            # Price history
            hist = t.history(period="1y")
            hist["returns"] = hist["Close"].pct_change()

            volatility = hist["returns"].std()

            # Drawdown
            rolling_max = hist["Close"].cummax()
            dd = (hist["Close"] - rolling_max) / rolling_max
            max_drawdown = dd.min()

            # Financial risk from BalanceSheetAgent
            bs = self.bs_agent.analyze_company(ticker)

            debt_to_equity = bs.get("debt_to_equity")
            current_ratio = bs.get("current_ratio")

            # Scores
            beta_score = self.score_inverse(beta, self.thresholds["beta"])
            volatility_score = self.score_inverse(volatility, self.thresholds["volatility"])
            drawdown_score = self.score_inverse(abs(max_drawdown), self.thresholds["drawdown"])
            debt_score = self.score_inverse(debt_to_equity, self.thresholds["debt_to_equity"])
            liquidity_score = self.score_inverse(current_ratio, self.thresholds["current_ratio"])

            risk_score = float(
                np.mean([
                    beta_score,
                    volatility_score,
                    drawdown_score,
                    debt_score,
                    liquidity_score
                ])
            )

            return {
                "beta": beta,
                "volatility": volatility,
                "max_drawdown": max_drawdown,
                "debt_to_equity": debt_to_equity,
                "current_ratio": current_ratio,
                "beta_score": beta_score,
                "volatility_score": volatility_score,
                "drawdown_score": drawdown_score,
                "debt_score": debt_score,
                "liquidity_score": liquidity_score,
                "risk_score": risk_score
            }

        except Exception as e:
            return {"error": str(e), "risk_score": 1}
