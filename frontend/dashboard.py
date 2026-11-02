import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st

from backend.strategy import analyze_latest, backtest_metrics, load_prices

prices = load_prices()

st.title("QQQ Multi-Agent Trading System")

if st.button("Analyze latest day"):
    result = analyze_latest(prices)
    decision = result["decision"]
    explanation = result.get("explanation")

    st.subheader(f"{result['date']}: {decision['label']}")
    st.caption(decision["reasoning"])

    if explanation:
        st.write(explanation["text"])
        if explanation["consistent"] is False:
            st.warning("Consistency check flagged this explanation: " + " ".join(explanation["issues"]))
        elif explanation["consistent"]:
            st.success(f"Consistency check passed ({explanation['attempts']} attempt(s)).")

    st.subheader("Agent signals")
    st.json({name: result[name] for name in ("technical", "sentiment", "risk")})

    st.subheader("News analysed")
    if result["headlines"]:
        for h in result["headlines"]:
            st.write(f"- {h['title']} ({h['source']})")
    else:
        st.write("No headlines available; sentiment and risk used price data.")

    st.subheader("Agent communication log")
    st.dataframe(pd.DataFrame(
        [{"step": e["step"], "sender": e["sender"], "timestamp": e["timestamp"], "content": str(e["content"])}
         for e in result["log"]]
    ))

if st.button("Run backtest"):
    result = backtest_metrics(prices)

    st.subheader("Backtest metrics")
    st.table(pd.DataFrame({
        "MAS strategy": result["strategy_metrics"],
        "QQQ buy-and-hold": result["benchmark_metrics"],
    }))
