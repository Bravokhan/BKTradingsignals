import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

# Title
st.title("📈 Forex 1-Min Candle Direction Predictor")

# Supported pairs (Yahoo tickers for forex)
pairs = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "NZD/USD": "NZDUSD=X"
}

# Dropdown
selected_pair = st.selectbox("Select Forex Pair", list(pairs.keys()))

if st.button("📊 Predict Next 1-Min Candle"):
    try:
        # Fetch last 2 minutes of 1min data
        ticker = yf.Ticker(pairs[selected_pair])
        df = ticker.history(interval="1m", period="2m")

        if len(df) >= 2:
            last_candle = df.iloc[-2]
            next_candle = df.iloc[-1]

            direction = "📈 UP" if next_candle["Close"] > last_candle["Close"] else "📉 DOWN"
            st.success(f"Next 1-min candle direction for {selected_pair}: **{direction}**")
        else:
            st.warning("⚠️ Not enough data to determine direction.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
