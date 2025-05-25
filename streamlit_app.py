import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import pytz

# Page config
st.set_page_config(page_title="PX Signal Bot", layout="wide")

# Heading
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>📈 PX Signal Bot - Live Trading Signals</h1>", unsafe_allow_html=True)

# Timezone display
local_tz = pytz.timezone('Asia/Karachi')
local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f"<p style='text-align:center;'>🕒 Local Time (UTC +05:00): <b>{local_time}</b></p>", unsafe_allow_html=True)

# Currency pairs
symbols = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "CAD=X",
    "EUR/JPY": "EURJPY=X"
}

# Pair selector
pair = st.selectbox("Select Forex Pair:", list(symbols.keys()))

# Button to fetch direction
if st.button("Get Next Candle Direction"):
    symbol = symbols[pair]
    try:
        df = yf.download(symbol, period="1d", interval="5m")  # Use 5-minute interval
        if df.empty:
            st.warning("⚠️ No data available for this pair.")
        else:
            # Use last two candles to determine direction
            last_candle = df.iloc[-1]
            prev_candle = df.iloc[-2]

            if last_candle["Close"] > last_candle["Open"]:
                direction = "📈 UP (Bullish)"
                color = "green"
            elif last_candle["Close"] < last_candle["Open"]:
                direction = "📉 DOWN (Bearish)"
                color = "red"
            else:
                direction = "➖ SIDEWAYS (Neutral)"
                color = "gray"

            st.markdown(f"<h2 style='color:{color}; text-align:center;'>Next Candle Likely Direction: {direction}</h2>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
