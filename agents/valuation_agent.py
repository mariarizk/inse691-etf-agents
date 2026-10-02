import yfinance as yf
import numpy as np

class ValuationAgent:
    def __init__(self, ratio_thresholds):
        """
        ratio_thresholds example:
        {
            "pe": {"good": 15, "neutral": 25},
            "peg": {"good": 1.0, "neutral": 1.5},
            "ps": {"good": 3.0, "neutral": 6.0},
            "pb": {"good": 3.0, "neutral": 6.0},
            "ev_ebitda": {"good": 10, "neutral": 15}
        }
        """
        self.thresholds = ratio_thresholds

    def score_inverse_ratio(self, value, thresholds):
        # lower is better
        if value is None or np.isnan(value):
            return 1
        if value <= thresholds["good"]:
            return 3
        elif value <= thresholds["neutral"]:
            return 2
        return 1

    def analyze_company(self, ticker):
        try:
            t = yf.Ticker(ticker)
            info = t.info if hasattr(t, "info") else t.get_info()

            pe = info.get("trailingPE")
            forward_pe = info.get("forwardPE")
            peg = info.get("pegRatio")
            ps = info.get("priceToSalesTrailing12Months")
            pb = info.get("priceToBook")
            ev_ebitda = info.get("enterpriseToEbitda")

            pe_score = self.score_inverse_ratio(pe, self.thresholds["pe"])
            peg_score = self.score_inverse_ratio(peg, self.thresholds["peg"])
            ps_score = self.score_inverse_ratio(ps, self.thresholds["ps"])
            pb_score = self.score_inverse_ratio(pb, self.thresholds["pb"])
            ev_ebitda_score = self.score_inverse_ratio(ev_ebitda, self.thresholds["ev_ebitda"])

            valuation_score = np.mean([
                pe_score,
                peg_score,
                ps_score,
                pb_score,
                ev_ebitda_score
            ])

            return {
                "pe": pe,
                "forward_pe": forward_pe,
                "peg": peg,
                "ps": ps,
                "pb": pb,
                "ev_ebitda": ev_ebitda,
                "pe_score": pe_score,
                "peg_score": peg_score,
                "ps_score": ps_score,
                "pb_score": pb_score,
                "ev_ebitda_score": ev_ebitda_score,
                "valuation_score": valuation_score
            }

        except Exception as e:
            return {"error": str(e), "valuation_score": 1}
