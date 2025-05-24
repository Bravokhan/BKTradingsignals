import streamlit as st
st.set_page_config(page_title="PX Signal Bot", layout="wide")

import yfinance as yf
import pandas as pd
import pandas_ta as ta
from streamlit_autorefresh import st_autorefresh

st.markdown("""<h1 style='text-align: center; color: #00ffcc;'>📈 PX Signal Bot - Live Trading Signals</h1>""", unsafe_allow_html=True)

# Display local time (UTC+5)
local_tz = pytz.timezone('Asia/Karachi')
local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f"<p style='text-align:center;'>🕒 Local Time (UTC +05:00): <b>{local_time}</b></p>", unsafe_allow_html=True)

symbols = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "CAD=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "EUR/USD (dup)": "EURUSD=X"
}

# Define signal function
def generate_signal(df):
    df.ta.rsi(length=14, append=True)
    df.ta.ema(length=9, append=True)
    df.ta.macd(append=True)

    last = df.iloc[-1]
    signal = "WAIT"

    if last['RSI_14'] < 30 and last['MACDh_12_26_9'] > 0 and last['Close'] > last['EMA_9']:
        signal = "UP"
    elif last['RSI_14'] > 70 and last['MACDh_12_26_9'] < 0 and last['Close'] < last['EMA_9']:
        signal = "DOWN"

    return signal

col1, col2 = st.columns(2)

with col1:
    st.subheader("1-Minute Signals")
    for name, ticker in symbols.items():
        df = yf.download(ticker, interval="1m", period="30m")
        if not df.empty:
            signal = generate_signal(df)
            color = {"UP": "green", "DOWN": "red", "WAIT": "gray"}[signal]
            st.markdown(f"<p style='color:{color};'><b>{name}:</b> {signal}</p>", unsafe_allow_html=True)

with col2:
    st.subheader("5-Minute Signals")
    for name, ticker in symbols.items():
        df = yf.download(ticker, interval="5m", period="2h")
        if not df.empty:
            signal = generate_signal(df)
            color = {"UP": "green", "DOWN": "red", "WAIT": "gray"}[signal]
            st.markdown(f"<p style='color:{color};'><b>{name}:</b> {signal}</p>", unsafe_allow_html=True)
