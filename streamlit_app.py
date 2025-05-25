import streamlit as st
import yfinance as yf
import pandas_ta as ta
from datetime import datetime, timedelta
import pytz

# Set Streamlit page config
st.set_page_config(page_title="PX Signal Bot", layout="wide")

# App Header
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>📈 PX Signal Bot - 1M Prediction</h1>", unsafe_allow_html=True)

# Timezone
local_tz = pytz.timezone("Asia/Karachi")

# Input for pair (e.g., BTC-USD)
symbol = st.selectbox("Select Pair:", ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD", "XRP-USD"])

# Button to trigger prediction
if st.button("🔎 Predict Next 1M Candle Direction"):
    try:
        # Get today's start time in UTC
        now = datetime.now(local_tz)
        today_start = datetime(now.year, now.month, now.day, tzinfo=local_tz).astimezone(pytz.utc)
        
        # Fetch 1m historical data
        data = yf.download(symbol, interval="1m", start=today_start, progress=False)

        if data.empty or len(data) < 5:
            st.warning("⚠️ No data available for this pair.")
        else:
            # Simple Strategy: Compare last two closes
            last = data["Close"].iloc[-1]
            prev = data["Close"].iloc[-2]

            if last > prev:
                st.success("📈 Predicted Direction: UP")
            elif last < prev:
                st.error("📉 Predicted Direction: DOWN")
            else:
                st.info("➡️ Predicted Direction: FLAT (No change)")

            # Optional: Display last 5 candles
            st.subheader("📊 Last 5 Candles")
            st.dataframe(data.tail())

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
