import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Set page configuration
st.set_page_config(page_title="PX Signal Bot", layout="wide")

# App title
st.markdown("""<h1 style='text-align: center; color: #00ffcc;'>📈 PX Signal Bot</h1>""", 
            unsafe_allow_html=True)

# Local time display
local_tz = pytz.timezone('Asia/Karachi')
local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f"<p style='text-align:center;'>🕒 Local Time: <b>{local_time}</b></p>", 
            unsafe_allow_html=True)

# Auto-refresh
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

# Main processing
for pair, symbol in symbols.items():
    try:
        # Get data with error handling
        data = yf.download(symbol, period="2d", interval=timeframe, progress=False)
        
        if data.empty or len(data) < 14:
            st.warning(f"⚠️ Insufficient data for {pair} ({timeframe} timeframe)")
            continue

        # Calculate indicators
        data["RSI"] = ta.rsi(data["Close"], length=14)
        data["EMA"] = ta.ema(data["Close"], length=14)
        
        # Get the latest values as scalars
        latest_close = float(data["Close"].iloc[-1])
        latest_ema = float(data["EMA"].iloc[-1])
        latest_rsi = float(data["RSI"].iloc[-1])

        # Generate signal (using scalar values)
        if pd.isna(latest_close) or pd.isna(latest_ema) or pd.isna(latest_rsi):
            signal = "⚪ WAIT (Missing Data)"
        elif latest_close > latest_ema and latest_rsi < 70:
            signal = "📈 BUY"
        elif latest_close < latest_ema and latest_rsi > 30:
            signal = "📉 SELL"
        else:
            signal = "⚪ WAIT"

        # Display results
        st.markdown(f"### {pair}")
        st.write(f"Price: {latest_close:.5f}")
        st.write(f"RSI: {latest_rsi:.2f}")
        st.write(f"EMA: {latest_ema:.5f}")
        st.markdown(f"**Signal: {signal}**")
        st.markdown("---")

    except Exception as e:
        st.error(f"❌ Error processing {pair}: {str(e)}")
        continue
