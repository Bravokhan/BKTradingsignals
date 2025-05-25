import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import pytz
from datetime import datetime

# Set page config (must be first)
st.set_page_config(page_title="PX Signal Bot", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>📊 PX Signal Bot - 1 Minute Candle Direction</h1>", unsafe_allow_html=True)

# Show current time
local_tz = pytz.timezone('Asia/Karachi')
local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f"<p style='text-align:center;'>🕒 Local Time (UTC +05:00): <b>{local_time}</b></p>", unsafe_allow_html=True)

# Available trading pairs
symbols = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "CAD=X",
    "BTC/USD": "BTC-USD",
    "ETH/USD": "ETH-USD"
}

# Select pair
pair_name = st.selectbox("Select Trading Pair", list(symbols.keys()))
selected_symbol = symbols[pair_name]

# Button to analyze
if st.button("📈 Check Next 1M Direction"):
    try:
        # Get recent 2 hours of 1-minute data
        df = yf.download(selected_symbol, period="2h", interval="1m")

        if df.empty:
            st.error("⚠️ No data available for this pair.")
        else:
            df["RSI"] = ta.rsi(df["Close"], length=14)
            df["EMA"] = ta.ema(df["Close"], length=14)
            latest = df.iloc[-1]

            # Signal logic
            if latest["Close"] > latest["EMA"] and latest["RSI"] < 70:
                signal = "📈 BUY (Up Direction Expected)"
            elif latest["Close"] < latest["EMA"] and latest["RSI"] > 30:
                signal = "📉 SELL (Down Direction Expected)"
            else:
                signal = "⚪ WAIT (No Clear Direction)"

            # Show results
            st.markdown(f"### 🔍 Pair: {pair_name}")
            st.write(f"Last Price: {latest['Close']:.5f}")
            st.write(f"RSI: {latest['RSI']:.2f}")
            st.write(f"EMA: {latest['EMA']:.5f}")
            st.markdown(f"## 📍 Signal: {signal}")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
