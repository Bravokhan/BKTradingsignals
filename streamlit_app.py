import streamlit as st
import yfinance as yf

st.set_page_config(page_title="1M Forex Signal", page_icon="📈")
st.title("📊 Forex 1-Min Candle Direction Predictor")

# Forex Pairs from Yahoo Finance
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

# Button to run prediction
if st.button("Predict Next 1-Min Candle"):
    with st.spinner("Fetching live data..."):
        try:
            ticker = yf.Ticker(pairs[selected_pair])
            df = ticker.history(period="2m", interval="1m")

            if df is None or df.empty or len(df) < 2:
                st.warning("⚠️ Not enough data to determine direction.")
            else:
                last = df.iloc[-2]
                current = df.iloc[-1]

                if current["Close"] > last["Close"]:
                    st.success(f"✅ Prediction: UP 📈")
                elif current["Close"] < last["Close"]:
                    st.success(f"✅ Prediction: DOWN 📉")
                else:
                    st.info("⚠️ No Movement: Same Close Price.")

                # Optional: Show raw data
                with st.expander("Show Raw Candle Data"):
                    st.dataframe(df)

        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")
