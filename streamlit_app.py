import streamlit as st
import random
import pandas as pd
import pytz
from datetime import datetime

# --- Beautiful Page Setup ---
st.set_page_config(
    page_title="🎯 Random Forex Signals",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
            
html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}
.header {
    font-size: 2.5rem !important;
    color: #4B32C3 !important;
    text-align: center;
    margin-bottom: 30px;
}
.signal-card {
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    text-align: center;
}
.call {
    background: linear-gradient(135deg, #6BFF97 0%, #00E676 100%);
    color: white;
}
.put {
    background: linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%);
    color: white;
}
.neutral {
    background: linear-gradient(135deg, #AEB6BF 0%, #85929E 100%);
    color: white;
}
.time-display {
    font-size: 1.2rem;
    color: #5D6D7E;
    text-align: center;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown('<p class="header">🎯 Random Forex Signal Generator</p>', unsafe_allow_html=True)

# Time Display
local_tz = pytz.timezone('Asia/Karachi')
current_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
st.markdown(f'<p class="time-display">🕒 Karachi Time: {current_time}</p>', unsafe_allow_html=True)

# --- Forex Pairs ---
forex_pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF", "NZD/USD"]

# --- Signal Generation ---
if st.button("🎲 Generate Random Signals", use_container_width=True):
    signals = []
    
    for pair in forex_pairs:
        # Random signal generation
        rand_num = random.random()
        
        if rand_num > 0.6:
            direction = "CALL"
            strength = random.choice(["STRONG", "MEDIUM"])
            css_class = "call"
        elif rand_num < 0.4:
            direction = "PUT"
            strength = random.choice(["STRONG", "MEDIUM"])
            css_class = "put"
        else:
            direction = "NEUTRAL"
            strength = "WAIT"
            css_class = "neutral"
        
        signals.append({
            "Pair": pair,
            "Direction": direction,
            "Strength": strength,
            "Class": css_class
        })
    
    # Display signals in cards
    cols = st.columns(2)
    for idx, signal in enumerate(signals):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="signal-card {signal['Class']}">
                    <h2>{signal['Pair']}</h2>
                    <h1>{signal['Direction']}</h1>
                    <h3>{signal['Strength']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Show history table
    st.markdown("---")
    st.subheader("📜 Signal History")
    history_df = pd.DataFrame(signals)
    st.dataframe(
        history_df[["Pair", "Direction", "Strength"]],
        use_container_width=True,
        hide_index=True
    )

# --- Sidebar Info ---
with st.sidebar:
    st.markdown("## ℹ️ About")
    st.markdown("""
    This bot generates **random forex signals** for demonstration purposes:
    - No API required
    - Pure random generation
    - Beautiful UI design
    """)
    st.markdown("---")
    st.markdown("### 🔄 Probability Settings")
    call_prob = st.slider("CALL Probability", 0, 100, 60)
    put_prob = st.slider("PUT Probability", 0, 100, 40)
    st.markdown("---")
    st.markdown("Created with ❤️ using Streamlit")

# --- How to Run ---
st.markdown("---")
st.markdown("### 💻 How to Run This App")
st.code("""
pip install streamlit pandas pytz
streamlit run forex_bot.py
""")
