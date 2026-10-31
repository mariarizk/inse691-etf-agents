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
    explanation = result["explanation"]

    st.subheader(f"{result['date']}: {final['label']} (decided by {final['source']})")
    st.caption(f"Rule-based decision: {result['rule_decision']['label']}")
    st.write(explanation["text"])

    if explanation["consistent"] is False:
        st.warning("Consistency guard flagged this explanation: " + " ".join(explanation["issues"]))
    elif explanation["consistent"]:
        st.success(f"Consistency guard passed ({explanation['attempts']} attempt(s)).")

    if final["note"]:
        st.warning(final["note"])

    st.subheader("Agent signals")
    st.json(result["signals"])

    news = result["signals"].get("news_sentiment")
    if news:
        st.subheader("News sentiment")
        st.write(news["summary"] or news["note"])

    if final["debate"]:
        st.subheader("Debate")
        st.json(final["debate"])

    st.subheader("Agent communication log")
    st.dataframe(pd.DataFrame(
        [{"step": e["step"], "sender": e["sender"], "timestamp": e["timestamp"], "content": str(e["content"])}
         for e in result["log"]]
    ))

if st.button("Run backtest report"):
    result = advisor.backtest_report(prices)

    st.subheader("Performance report")
    st.write(result["report"])

    st.subheader("Metrics")
    st.table(pd.DataFrame({
        "MAS strategy": result["strategy_metrics"],
        "QQQ buy-and-hold": result["benchmark_metrics"],
    }))
