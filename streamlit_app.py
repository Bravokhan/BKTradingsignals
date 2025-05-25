import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz

st.set_page_config(page_title="📈 Forex Signal Bot", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #00ffcc;'>📈 Forex Signal Bot - 1M Direction</h1>
""", unsafe_allow_html=True)

# Define timezone
local_tz = pytz.timezone('Asia/Karachi')

# Select forex pair
selected_pair = st.selectbox("Select Forex Pair:", [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"
])

if st.button("Get 1M Candle Direction"):
    try:
        # Define TradingView symbol format
        symbol_map = {
            "EURUSD": "FX:EURUSD",
            "GBPUSD": "FX:GBPUSD",
            "USDJPY": "FX:USDJPY",
            "AUDUSD": "FX:AUDUSD",
            "USDCHF": "FX:USDCHF"
        }

        symbol = symbol_map[selected_pair]

        # TradingView API-like structure using a public source (simulated)
        url = f"https://api.binance.com/api/v3/klines?symbol={selected_pair.replace('/', '')}T&interval=1m&limit=20"
        response = requests.get(url)

        if response.status_code != 200:
            st.error("❌ Failed to fetch data from Binance API.")
        else:
            data = response.json()
            df = pd.DataFrame(data, columns=[
                'time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base', 'taker_buy_quote', 'ignore'
            ])
            df['close'] = pd.to_numeric(df['close'])
            df['open'] = pd.to_numeric(df['open'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')

            last_candle = df.iloc[-1]
            close = last_candle['close']
            open_price = last_candle['open']

            if close > open_price:
                st.success(f"📈 Next 1M Candle Direction for {selected_pair}: UP")
            elif close < open_price:
                st.error(f"📉 Next 1M Candle Direction for {selected_pair}: DOWN")
            else:
                st.info(f"➖ Next 1M Candle Direction for {selected_pair}: NEUTRAL")

    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
