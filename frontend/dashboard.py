import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st

from backend.advisor import Advisor
from backend.strategy import load_prices

advisor = Advisor()
prices = load_prices()

st.title("QQQ Multi-Agent Trading System")

if st.button("Analyze latest day"):
    result = advisor.analyze_latest(prices)
    final = result["final_decision"]

    st.subheader(f"{result['date']}: {final['label']} (decided by {final['source']})")
    st.write(result["explanation"])
    if final["note"]:
        st.warning(final["note"])

    st.subheader("Agent signals")
    st.json(result["signals"])

    if final["debate"]:
        st.subheader("Debate")
        st.json(final["debate"])

if st.button("Run backtest report"):
    result = advisor.backtest_report(prices)

    st.subheader("Performance report")
    st.write(result["report"])

    st.subheader("Metrics")
    st.table(pd.DataFrame({
        "MAS strategy": result["strategy_metrics"],
        "QQQ buy-and-hold": result["benchmark_metrics"],
    }))
