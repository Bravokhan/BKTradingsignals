import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="PX Signal Bot", layout="wide")

# App title
st.markdown("""<h1 style='text-align: center; color: #00ffcc;'>📈 PX Signal Bot - Live Trading Signals</h1>""", unsafe_allow_html=True)

# Display local time (UTC+5)
local_tz = pytz.timezone('Asia/Karachi')
local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f"<p style='text-align:center;'>🕒 Local Time (UTC +05:00): <b>{local_time}</b></p>", unsafe_allow_html=True)

# Auto refresh every 60 seconds
st_autorefresh(interval=60000, key="auto_refresh")

# Forex and crypto symbols
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
    "BTC/USD": "BTC-USD",
    "ETH/USD": "ETH-USD"
}

# Timeframe selection
timeframe = st.selectbox("Select Timeframe", ["5m", "15m", "1h", "1d"])

# Loop through symbols and show signals
for pair, symbol in symbols.items():
    try:
        data = yf.download(symbol, period="2d", interval=timeframe)
        if data.empty:
            st.warning(f"No data found for {pair}")
            continue

        data["RSI"] = ta.rsi(data["Close"], length=14)
        data["EMA"] = ta.ema(data["Close"], length=14)
        latest = data.iloc[-1]

        # Generate signal
        if latest["Close"] > latest["EMA"] and latest["RSI"] < 70:
            signal = "📈 BUY"
        elif latest["Close"] < latest["EMA"] and latest["RSI"] > 30:
            signal = "📉 SELL"
        else:
            signal = "⚪ WAIT"

        # Display results
        st.markdown(f"### {pair}")
        st.write(f"Last Price: {latest['Close']:.4f}")
        st.write(f"RSI: {latest['RSI']:.2f}")
        st.write(f"EMA: {latest['EMA']:.4f}")
        st.markdown(f"**Signal: {signal}**")
        st.markdown("---")

    except Exception as e:
        st.error(f"Error for {pair}: {str(e)}")
