import pandas as pd

class Backtester:
    """
    Backtester (MAS Version)
    ------------------------
    Supports BUY (1), HOLD (0), SELL (-1) signals.
    Computes positions, daily returns, and equity curve.
    """

    def __init__(self, price_df, decisions):
        self.df = price_df.copy()
        self.decisions = decisions

    def _extract_actions(self):
        """Convert decision list into a position series."""
        # decisions is a list of dicts: {"action": int}
        actions = [d["action"] for d in self.decisions]

        return pd.Series(actions, index=self.df.index)

    def _compute_returns(self, positions):
        """Compute daily strategy returns."""
        # daily returns of QQQ
        self.df["returns"] = self.df["Close"].pct_change()

        # strategy return = position[t-1] * daily_return[t]
        strat_returns = positions.shift(1) * self.df["returns"]
        strat_returns.fillna(0, inplace=True)

        return strat_returns

    def _compute_equity_curve(self, strat_returns):
        """Compute cumulative equity curve."""
        equity = (1 + strat_returns).cumprod()
        return equity

    def run(self):
        """Main entry point."""
        positions = self._extract_actions()
        strat_returns = self._compute_returns(positions)
        equity_curve = self._compute_equity_curve(strat_returns)

        return {
            "positions": positions,
            "returns": strat_returns,
            "equity_curve": equity_curve
        }
