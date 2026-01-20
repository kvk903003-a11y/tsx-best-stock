import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Best Stock to Buy Now", layout="centered")

st.title("📈 Best Stock to Buy Now (Simple)")

# Load tickers safely
try:
    tickers = pd.read_csv("data/tsx_tickers.csv", header=None)[0].tolist()
except Exception as e:
    st.error("Ticker file not found or invalid.")
    st.stop()

results = []

st.write("Analyzing stocks... please wait ⏳")

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")

        if hist.empty:
            continue

        change = (hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0] * 100

        results.append({
            "Ticker": ticker,
            "Price": round(hist["Close"].iloc[-1], 2),
            "5D % Change": round(change, 2)
        })
    except:
        continue

if not results:
    st.warning("No data available right now.")
    st.stop()

df = pd.DataFrame(results)
best = df.sort_values("5D % Change", ascending=False).iloc[0]

st.success("✅ BEST STOCK RIGHT NOW")

st.metric("Stock", best["Ticker"])
st.metric("Current Price", f"${best['Price']}")
st.metric("5-Day Change", f"{best['5D % Change']}%")

st.caption("Data source: Yahoo Finance")
