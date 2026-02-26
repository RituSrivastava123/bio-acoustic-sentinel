import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import time
import random
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

# =============================
# GLOBAL STYLING
# =============================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

h1, h2, h3 {
    color: #00ffcc;
}

/* Azure Header */
.azure-header {
    background: linear-gradient(90deg, #0078D4, #00BCF2);
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
    color: white;
    font-size: 20px;
}

/* Emergency takeover */
.emergency {
    background-color: #8B0000 !important;
    color: white !important;
    padding: 20px;
    border-radius: 10px;
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0% { background-color: #8B0000; }
    50% { background-color: #FF0000; }
    100% { background-color: #8B0000; }
}

/* Animated siren icon */
.siren {
    font-size: 50px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(-10deg); }
    50% { transform: rotate(10deg); }
    100% { transform: rotate(-10deg); }
}

/* Buttons */
div.stButton > button {
    background-color: #ff0033;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
}

div.stDownloadButton > button {
    background-color: #00cc99;
    color: black;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# SESSION STATE
# =============================
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "emergency" not in st.session_state:
    st.session_state.emergency = False

if "alert_history" not in st.session_state:
    st.session_state.alert_history = []

if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0
if "threats_detected" not in st.session_state:
    st.session_state.threats_detected = 0
if "high_alerts" not in st.session_state:
    st.session_state.high_alerts = 0

# =============================
# AZURE HEADER
# =============================
st.markdown('<div class="azure-header">☁ Microsoft Azure Smart Forest Monitoring Network</div>', unsafe_allow_html=True)

st.title("🌱 Bio-Acoustic Sentinel")

# =============================
# UPTIME
# =============================
uptime = int(time.time() - st.session_state.start_time)
st.caption(f"🕒 System Uptime: {uptime} seconds")

# =============================
# SIDEBAR
# =============================
st.sidebar.header("🛠 Controls")

region = st.sidebar.selectbox(
    "🌍 Forest Region",
    ["Uttarakhand", "Assam", "Amazon", "Sundarbans", "Western Ghats"]
)

st.sidebar.success("🟢 System Status: ACTIVE")

# =============================
# DASHBOARD METRICS
# =============================
col1, col2, col3 = st.columns(3)
col1.metric("🔎 Total Scans", st.session_state.total_scans)
col2.metric("🚨 Threats Detected", st.session_state.threats_detected)
col3.metric("🔥 High Escalations", st.session_state.high_alerts)

st.divider()

# =============================
# SIMULATE HIGH ALERT
# =============================
simulate = st.button("🚨 Simulate HIGH ALERT")

if simulate:
    st.session_state.emergency = True
    st.session_state.total_scans += 1
    st.session_state.threats_detected += 1
    st.session_state.high_alerts += 1

    alert_entry = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Region": region,
        "Threat": "Chainsaw",
        "Confidence (%)": 95
    }
    st.session_state.alert_history.append(alert_entry)

# =============================
# EMERGENCY MODE DISPLAY
# =============================
if st.session_state.emergency:

    st.markdown('<div class="emergency">', unsafe_allow_html=True)

    st.markdown('<div class="siren">🚨</div>', unsafe_allow_html=True)

    st.error(f"HIGH ALERT: Chainsaw detected in {region}")
    st.info("📧 Email Notification Sent (Simulated Azure Logic App)")

    # Siren Sound
    st.markdown("""
    <audio autoplay>
        <source src="https://www.soundjay.com/misc/sounds/siren-01.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

    # Confidence Gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=95,
        title={'text': "AI Confidence"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "cyan"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "red"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Auto reset after 5 seconds
    time.sleep(5)
    st.session_state.emergency = False
    st.experimental_rerun()

# =============================
# ALERT HISTORY
# =============================
if st.session_state.alert_history:
    st.subheader("🗂 Alert History")
    history_df = pd.DataFrame(st.session_state.alert_history)
    st.dataframe(history_df, use_container_width=True)

    # PDF Export
    def generate_pdf(dataframe):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "Bio-Acoustic Sentinel Alert Report")
        y = 720
        for index, row in dataframe.iterrows():
            text = f"{row['Time']} | {row['Region']} | {row['Threat']} | {row['Confidence (%)']}%"
            p.drawString(50, y, text)
            y -= 20
        p.save()
        buffer.seek(0)
        return buffer

    pdf = generate_pdf(history_df)

    st.download_button(
        label="📄 Download Alert Report (PDF)",
        data=pdf,
        file_name="alert_report.pdf",
        mime="application/pdf"
    )

st.info("Press 'Simulate HIGH ALERT' to demonstrate emergency response.")
