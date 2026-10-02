import numpy as np
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from agents.balance_sheet_agent import BalanceSheetAgent
from agents.income_statement_agent import IncomeStatementAgent
from agents.cash_flow_agent import CashFlowAgent
from agents.valuation_agent import ValuationAgent
from agents.efficiency_agent import EfficiencyAgent


class FundamentalAgent:
    def __init__(
        self,
        balance_sheet_thresholds,
        income_statement_thresholds,
        cashflow_thresholds,
        valuation_thresholds,
        efficiency_thresholds,
    ):
        self.balance_sheet_agent = BalanceSheetAgent(balance_sheet_thresholds)
        self.income_statement_agent = IncomeStatementAgent(income_statement_thresholds)
        self.cashflow_agent = CashFlowAgent(cashflow_thresholds)
        self.valuation_agent = ValuationAgent(valuation_thresholds)
        self.efficiency_agent = EfficiencyAgent(efficiency_thresholds)

    def analyze_company(self, ticker):
        try:
            bs_result = self.balance_sheet_agent.analyze_company(ticker)
            is_result = self.income_statement_agent.analyze_company(ticker)
            cf_result = self.cashflow_agent.analyze_company(ticker)
            val_result = self.valuation_agent.analyze_company(ticker)
            eff_result = self.efficiency_agent.analyze_company(ticker)

            # if any sub‑agent failed, propagate a safe fallback
            for r in [bs_result, is_result, cf_result, val_result, eff_result]:
                if "error" in r:
                    return {
                        "error": "One or more fundamental sub‑agents failed",
                        "fundamental_score": 1,
                        "balance_sheet": bs_result,
                        "income_statement": is_result,
                        "cashflow": cf_result,
                        "valuation": val_result,
                        "efficiency": eff_result,
                    }

            balance_sheet_score = bs_result["balance_sheet_score"]
            income_statement_score = is_result["income_statement_score"]
            cashflow_score = cf_result["cashflow_score"]
            valuation_score = val_result["valuation_score"]
            efficiency_score = eff_result["efficiency_score"]

            fundamental_score = float(
                np.mean(
                    [
                        balance_sheet_score,
                        income_statement_score,
                        cashflow_score,
                        valuation_score,
                        efficiency_score,
                    ]
                )
            )

            return {
                "balance_sheet_score": balance_sheet_score,
                "income_statement_score": income_statement_score,
                "cashflow_score": cashflow_score,
                "valuation_score": valuation_score,
                "efficiency_score": efficiency_score,
                "fundamental_score": fundamental_score,
                "balance_sheet": bs_result,
                "income_statement": is_result,
                "cashflow": cf_result,
                "valuation": val_result,
                "efficiency": eff_result,
            }

        except Exception as e:
            return {"error": str(e), "fundamental_score": 1}
