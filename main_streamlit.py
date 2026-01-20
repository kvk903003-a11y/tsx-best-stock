import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="TSX Best Stock", layout="wide")

st.title("🇨🇦 TSX Best Stock to Buy Now")

@st.cache_data
def load_tickers():
    return pd.read_csv("data/tsx_tickers.csv")["Ticker"].tolist()

@st.cache_data
def get_data(ticker):
    return yf.download(ticker, period="5d", interval="5m")

tickers = load_tickers()
results = []

for t in tickers:
    try:
        df = get_data(t)
        if len(df) < 2:
            continue
        change = (df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2] * 100
        results.append({
            "Ticker": t,
            "Price": round(df["Close"].iloc[-1], 2),
            "Change %": round(change, 2)
        })
    except:
        pass

if results:
    df = pd.DataFrame(results).sort_values("Change %", ascending=False)
    best = df.iloc[0]

    st.subheader("✅ Best Stock Right Now")
    st.metric("Ticker", best["Ticker"])
    st.metric("Price", best["Price"])
    st.metric("Change %", best["Change %"])

    st.subheader("📊 All Stocks")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data available yet.")
