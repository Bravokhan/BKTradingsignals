import streamlit as st
from tvDatafeed import TvDatafeed, Interval
import datetime
import pytz

# ---- PAGE CONFIG ----
st.set_page_config(page_title="PX Signal Bot", layout="wide")

# ---- HEADER ----
st.markdown("<h2 style='text-align: center; color: #00ffcc;'>📊 PX Signal Bot — Next 1-Minute Candle Prediction</h2>", unsafe_allow_html=True)

# ---- LOGIN TO TRADINGVIEW ----
tv = TvDatafeed()  # Works without credentials unless restricted

# ---- PAIR MAPPING (TRADINGVIEW format) ----
pair_mapping = {
    "EUR/USD": ("OANDA", "EURUSD"),
    "GBP/USD": ("OANDA", "GBPUSD"),
    "USD/JPY": ("OANDA", "USDJPY"),
    "USD/CHF": ("OANDA", "USDCHF"),
    "AUD/USD": ("OANDA", "AUDUSD"),
    "USD/CAD": ("OANDA", "USDCAD"),
    "NZD/USD": ("OANDA", "NZDUSD")
}

# ---- PAIR SELECTION ----
selected_pair = st.selectbox("🔍 Select Forex Pair", list(pair_mapping.keys()))
symbol_info = pair_mapping[selected_pair]

# ---- BUTTON TO RUN ANALYSIS ----
if st.button("📈 Predict Next 1-Minute Candle"):

    try:
        # Get timezone-aware current time
        tz = pytz.timezone('UTC')
        now = datetime.datetime.now(tz)
        to_date = now.strftime('%Y-%m-%d %H:%M:%S')

        # Fetch last 6 candles of 1-minute timeframe
        data = tv.get_hist(symbol=symbol_info[1], exchange=symbol_info[0], interval=Interval.in_1_minute, n_bars=6)

        if data is None or data.empty:
            st.error("⚠️ No data received from TradingView.")
        else:
            # Use last 5 full candles for trend detection
            df = data.iloc[:-1]  # Exclude current forming candle
            ups = df[df['close'] > df['open']]
            downs = df[df['close'] < df['open']]

            if len(ups) > len(downs):
                st.success("⬆️ Predicted Direction: **Buy** (Bullish)")
            elif len(downs) > len(ups):
                st.error("⬇️ Predicted Direction: **Sell** (Bearish)")
            else:
                st.warning("➖ Predicted Direction: **Sideways / Uncertain**")

            # Optional: Show candle data
            with st.expander("📊 View Recent Candle Data"):
                st.dataframe(df[['open', 'high', 'low', 'close']])

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
