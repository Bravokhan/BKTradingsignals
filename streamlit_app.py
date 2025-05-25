import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz

# Set Streamlit page config (must be first Streamlit command)
st.set_page_config(page_title="PX Signal Bot", layout="wide")

# Page Title
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>📈 PX Signal Bot - Live Trading Signals</h1>", unsafe_allow_html=True)

# Show Local Time
local_tz = pytz.timezone('Asia/Karachi')
local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f"<p style='text-align:center;'>🕒 Local Time (UTC +05:00): <b>{local_time}</b></p>", unsafe_allow_html=True)

# Currency Pairs Dictionary
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

# User Selects Pair
pair = st.selectbox("Select Forex Pair:", list(symbols.keys()))

# Button to Fetch Direction
if st.button("Get Next Candle Direction"):
    symbol = symbols[pair]
    try:
        # Try fetching 5-minute interval data (1-day only)
        df = yf.download(symbol, period="1d", interval="5m")

        # If no data is returned
        if df.empty:
            st.warning("⚠️ No data available for this pair.")
        else:
            # Get last 2 completed candles
            last_candle = df.iloc[-1]
            prev_candle = df.iloc[-2]

            # Determine direction from last candle
            open_price = last_candle["Open"]
            close_price = last_candle["Close"]

            if close_price > open_price:
                direction = "📈 UP (Bullish)"
                color = "green"
            elif close_price < open_price:
                direction = "📉 DOWN (Bearish)"
                color = "red"
            else:
                direction = "➖ SIDEWAYS (Neutral)"
                color = "gray"

            st.markdown(f"<h2 style='color:{color}; text-align:center;'>Next Candle Likely Direction: {direction}</h2>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
