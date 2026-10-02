# Multi‑Agent System (MAS) for QQQ ETF Trading

This project implements a simple, interpretable Multi‑Agent System (MAS) that analyzes the QQQ ETF and generates daily BUY, HOLD, or SELL signals. The system is designed for academic use and demonstrates how multiple lightweight agents can collaborate to form a trading decision.

The MAS processes historical QQQ price data, produces daily signals, runs a full backtest, and generates performance plots such as equity curve, drawdown, rolling volatility, rolling Sharpe ratio, and a comparison against QQQ buy‑and‑hold.

---

## 🧠 Agents Overview

The system uses **four agents**, each responsible for one part of the decision-making process:

### 1. TechnicalAgent
Identifies market trend direction using moving‑average crossovers:
- Bullish  
- Neutral  
- Bearish  

### 2. SentimentAgent
Uses recent price returns as a simple sentiment indicator:
- Positive  
- Neutral  
- Negative  

### 3. RiskAgent
Measures volatility and classifies market risk:
- Low  
- Medium  
- High  

### 4. DecisionAgent
Combines all agent outputs and produces the final trading action:
- `1` → BUY  
- `0` → HOLD  
- `-1` → SELL


## ▶️ How to Run the Project

### 1. Activate your virtual environment
Windows:
```bash
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

"""Run the MAS pipeline"""
python scripts/run_pipeline.py
"""Run the backtest"""
python scripts/run_backtest.py
"""Generate plots"""
python scripts/plot_equity.py
python scripts/plot_drawdown.py
python scripts/plot_returns_histogram.py
python scripts/plot_rolling_metrics.py
python scripts/compare_vs_buyhold.py


