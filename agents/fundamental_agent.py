import yfinance as yf

class FundamentalAgent:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.Ticker(self.ticker).info
            return True
        except Exception as e:
            print("Error fetching data:", e)
            return False

    def get_basic_ratios(self):
        if not self.data:
            return None

        return {
            "market_cap": self.data.get("marketCap"),
            "pe_ratio": self.data.get("trailingPE"),
            "pb_ratio": self.data.get("priceToBook"),
            "dividend_yield": self.data.get("dividendYield"),
        }

    def analyze(self):
        ratios = self.get_basic_ratios()
        if ratios is None:
            return "No data available."

        analysis = []

        if ratios["pe_ratio"] and ratios["pe_ratio"] < 20:
            analysis.append("PE ratio indicates fair valuation.")
        else:
            analysis.append("PE ratio indicates possible overvaluation.")

        if ratios["pb_ratio"] and ratios["pb_ratio"] < 5:
            analysis.append("PB ratio is within a healthy range.")
        else:
            analysis.append("PB ratio may be high.")

        return analysis
    
    def summary(self):
        ratios = self.get_basic_ratios()
        analysis = self.analyze()

        # Determine a simple rating
        rating = "Neutral"
        if isinstance(analysis, list):
            if "fair valuation" in analysis[0]:
                rating = "Bullish"
            elif "overvaluation" in analysis[0]:
                rating = "Bearish"

        # Convert rating → numeric score
        if rating == "Bullish":
            score = 1
        elif rating == "Bearish":
            score = -1
        else:
            score = 0

        return {
            "ticker": self.ticker,
            "ratios": ratios,
            "analysis": analysis,
            "rating": rating,
            "score": score        # ⭐ REQUIRED by DecisionAgent
        }


    def score(self):
        score = 0

        # Example scoring logic
        if self.pe_ratio < 20:
            score += 1
        if self.eps > 0:
            score += 1
        if self.growth > 0.05:
            score += 1

        return score


