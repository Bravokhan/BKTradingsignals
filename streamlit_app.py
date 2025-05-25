import streamlit as st
import requests
import pandas as pd
import pytz
from datetime import datetime

# --- Setup ---
st.set_page_config(page_title="📈 Forex Signal Bot", layout="wide")
st.title("📈 Forex Signal Bot - 1M Direction")

API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
SYMBOLS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF"]
local_tz = pytz.timezone('Asia/Karachi')

# Symbol Mapping (Remove slashes)
SYMBOL_MAP = {pair: pair.replace("/", "") for pair in SYMBOLS}

def get_forex_data(symbol):
    mapped_symbol = SYMBOL_MAP[symbol]
    url = f"https://api.twelvedata.com/time_series?symbol={mapped_symbol}&interval=1min&outputsize=2&apikey={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'values' in data and len(data['values']) > 0:
                df = pd.DataFrame(data['values'])
                df['datetime'] = pd.to_datetime(df['datetime'])
                df['close'] = pd.to_numeric(df['close'])
                df['open'] = pd.to_numeric(df['open'])
                return df.iloc[-1]
            else:
                st.warning(f"⚠️ No candle data found for {symbol}")
        else:
            st.error(f"❌ API Error (Status: {response.status_code})")
    except Exception as e:
        st.error(f"❌ Connection Error: {str(e)}")
    return None

# --- Main App ---
selected_pair = st.selectbox("Select Forex Pair:", SYMBOLS)

if st.button("Get 1M Candle Direction"):
    with st.spinner("Fetching data..."):
        latest_candle = get_forex_data(selected_pair)
        
        if latest_candle is not None:
            st.markdown(f"### {selected_pair} - Last Candle (1M)")
            col1, col2 = st.columns(2)
            col1.metric("Open", f"{latest_candle['open']:.5f}")
            col2.metric("Close", f"{latest_candle['close']:.5f}")
            
            if latest_candle['close'] > latest_candle['open']:
                st.success("📈 Direction: UP (Green Candle)")
            elif latest_candle['close'] < latest_candle['open']:
                st.error("📉 Direction: DOWN (Red Candle)")
            else:
                st.info("➖ Direction: NEUTRAL (Doji)")
            
            local_time = latest_candle['datetime'].astimezone(local_tz)
            st.caption(f"Last update: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")

# --- API Key Help ---
st.markdown("---")
st.markdown("""
**How to get your API key:**
1. Sign up at [Twelve Data](https://twelvedata.com/)
2. Get your free API key from the dashboard
3. Replace `YOUR_API_KEY` in the code
""")
