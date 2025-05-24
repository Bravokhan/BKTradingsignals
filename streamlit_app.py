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
st.markdown("""<h1 style='text-align: center; color: #00ffcc;'>📈 PX Signal Bot - Live Trading Signals</h1>""", 
            unsafe_allow_html=True)

# Display local time (UTC+5)
local_tz = pytz.timezone('Asia/Karachi')
local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f"<p style='text-align:center;'>🕒 Local Time (UTC +05:00): <b>{local_time}</b></p>", 
            unsafe_allow_html=True)

# Auto refresh every 60 seconds
st_autorefresh(interval=60000, key="auto_refresh")

# Forex and crypto symbols with proper Yahoo Finance symbols
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

# Create empty DataFrame to store all signals
all_signals = pd.DataFrame(columns=["Pair", "Price", "RSI", "EMA", "Signal"])

# Loop through symbols and show signals
for pair, symbol in symbols.items():
    try:
        # Get data with timeout and error handling
        data = yf.download(symbol, period="2d", interval=timeframe, progress=False)
        
        if data.empty or len(data) < 14:  # Ensure enough data for indicators
            st.warning(f"⚠️ Insufficient data for {pair} ({timeframe} timeframe)")
            continue

        # Calculate indicators
        data["RSI"] = ta.rsi(data["Close"], length=14)
        data["EMA"] = ta.ema(data["Close"], length=14)
        latest = data.iloc[-1]

        # Generate signal with improved logic
        if pd.isna(latest["RSI"]) or pd.isna(latest["EMA"]):
            signal = "⚪ WAIT (No Data)"
        elif latest["Close"] > latest["EMA"] and latest["RSI"] < 70:
            signal = "📈 BUY"
        elif latest["Close"] < latest["EMA"] and latest["RSI"] > 30:
            signal = "📉 SELL"
        else:
            signal = "⚪ WAIT"

        # Store signals
        all_signals.loc[len(all_signals)] = [
            pair,
            f"{latest['Close']:.4f}",
            f"{latest['RSI']:.2f}",
            f"{latest['EMA']:.4f}",
            signal
        ]

    except Exception as e:
        st.error(f"❌ Error processing {pair}: {str(e)}")
        continue

# Display all signals in a clean table
if not all_signals.empty:
    st.markdown("### 📊 Current Signals Summary")
    st.dataframe(all_signals.style.applymap(
        lambda x: "color: green" if "BUY" in x else ("color: red" if "SELL" in x else "color: gray"),
        subset=["Signal"]
    ))
else:
    st.warning("No signals generated - check data connections")

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)
