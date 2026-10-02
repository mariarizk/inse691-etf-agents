import streamlit as st
from backend.etf_pipeline import ETFMultiAgentSystem
from config import CONFIG

system = ETFMultiAgentSystem(CONFIG)

st.title("ETF Multi-Agent Decision System")

ticker = st.text_input("Ticker", "AAPL")

if st.button("Run"):
    result = system.run(ticker)
    st.subheader("Decision")
    st.json(result["decision"])

    st.subheader("Agents")
    st.json(result["agents"])

tickers = st.text_input("Portfolio tickers (comma-separated)", "QQQ,TQQQ,SQQQ")

if st.button("Run Portfolio"):
    t_list = [t.strip() for t in tickers.split(",")]
    result = system.run_many(t_list)
    st.subheader("Portfolio Decision")
    st.json(result["portfolio_decision"])
    st.subheader("Per Ticker")
    st.json(result["per_ticker"])
