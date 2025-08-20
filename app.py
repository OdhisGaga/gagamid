import streamlit as st
import yfinance as yf
from strategy import generate_signal

st.set_page_config(page_title="Xgaga Tech Analysis", layout="wide")
st.title("📊 Xgaga Tech Analysis")

pairs = {
    'USD/AUD': 'AUDUSD=X',
    'JPY/AUD': 'AUDJPY=X',
    'EUR/USD': 'EURUSD=X',
    'GBP/USD': 'GBPUSD=X',
    'NZD/USD': 'NZDUSD=X'
}

timeframes = {
    '1 Minute': '1m',
    '5 Minutes': '5m',
    '15 Minutes': '15m',
    '1 Hour': '1h',
    '4 Hours': '4h',
    '1 Day': '1d',
    '1 Week': '1wk',
    '1 Month': '1mo'
}

for name, symbol in pairs.items():
    st.subheader(f"{name} — Tap to view signal")
    for label, tf in timeframes.items():
        df = yf.download(symbol, interval=tf, period='7d')
        if df.empty:
            continue
        signal = generate_signal(df)
        st.write(f"**{label}**: {signal}")
        st.line_chart(df['Close'])

