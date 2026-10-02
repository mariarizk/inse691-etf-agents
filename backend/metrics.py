import numpy as np
import pandas as pd

def compute_total_return(equity_curve):
    return equity_curve.iloc[-1] - 1.0

def compute_cagr(equity_curve):
    days = (equity_curve.index[-1] - equity_curve.index[0]).days
    years = days / 365.25
    return (equity_curve.iloc[-1]) ** (1 / years) - 1

def compute_volatility(returns):
    return returns.std() * np.sqrt(252)

def compute_sharpe(returns, risk_free_rate=0.02):
    excess = returns - (risk_free_rate / 252)
    return (excess.mean() / returns.std()) * np.sqrt(252)

def compute_max_drawdown(equity_curve):
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    return drawdown.min()

def compute_calmar(cagr, max_dd):
    return cagr / abs(max_dd) if max_dd != 0 else np.nan

def compute_all_metrics(equity_curve, returns):
    total_return = compute_total_return(equity_curve)
    cagr = compute_cagr(equity_curve)
    vol = compute_volatility(returns)
    sharpe = compute_sharpe(returns)
    max_dd = compute_max_drawdown(equity_curve)
    calmar = compute_calmar(cagr, max_dd)

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Volatility": vol,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd,
        "Calmar Ratio": calmar,
        "Mean Daily Return": returns.mean(),
        "Std Daily Return": returns.std()
    }
