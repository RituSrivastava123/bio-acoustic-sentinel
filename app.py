import streamlit as st
import numpy as np
import pandas as pd
import librosa
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
import random
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

# =============================
# CYBER DARK THEME
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
.blink {
    animation: blinker 1s linear infinite;
    border: 5px solid red;
    padding: 10px;
}
@keyframes blinker {
    50% { border-color: transparent; }
}
</style>
""", unsafe_allow_html=True)

# =============================
# SESSION STATE INIT
# =============================
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0
if "threats_detected" not in st.session_state:
    st.session_state.threats_detected = 0
if "high_alerts" not in st.session_state:
    st.session_state.high_alerts = 0
if "alert_history" not in st.session_state:
    st.session_state.alert_history = []
if "blink" not in st.session_state:
    st.session_state.blink = False

# =============================
# CONFIG
# =============================
THREAT_KEYWORDS = ["Chainsaw", "Gunshot", "Explosion", "Fire", "Siren"]
CONFIDENCE_THRESHOLD = 0.6

# =============================
# HEADER
# =============================
if st.session_state.blink:
    st.markdown('<div class="blink">', unsafe_allow_html=True)

st.title("🌱 Bio-Acoustic Sentinel")
st.markdown("☁ Powered by Microsoft Azure AI Infrastructure (Simulation)")
st.markdown("AI-powered Real-Time Environmental Threat Detection System")

if st.session_state.blink:
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# SYSTEM UPTIME
# =============================
uptime_seconds = int(time.time() - st.session_state.start_time)
st.caption(f"🕒 System Uptime: {uptime_seconds} seconds")

# =============================
# SIDEBAR
# =============================
st.sidebar.header("🛠 System Controls")
sensitivity = st.sidebar.slider("Detection Sensitivity", 0, 100, 75)

region = st.sidebar.selectbox(
    "🌍 Forest Region",
    ["Uttarakhand", "Assam", "Amazon", "Sundarbans", "Western Ghats"]
)

st.sidebar.success("🟢 System Status: ACTIVE")

# =============================
# MULTI SENSOR SIMULATION
# =============================
st.sidebar.subheader("📡 Sensor Network Status")
sensor_status = {
    "Sensor-1": random.choice(["Online", "Online", "Online", "Offline"]),
    "Sensor-2": random.choice(["Online", "Online", "Offline"]),
    "Sensor-3": random.choice(["Online", "Online", "Online"]),
}
for sensor, status in sensor_status.items():
    if status == "Online":
        st.sidebar.success(f"{sensor}: {status}")
    else:
        st.sidebar.error(f"{sensor}: {status}")

# =============================
# DASHBOARD METRICS
# =============================
st.divider()
st.subheader("📊 Real-Time Monitoring Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("🔎 Total Scans", st.session_state.total_scans)
col2.metric("🚨 Threats Detected", st.session_state.threats_detected)
col3.metric("🔥 High Escalations", st.session_state.high_alerts)

# =============================
# MAP
# =============================
st.subheader("🌍 Threat Monitoring Map")

region_coords = {
    "Uttarakhand": [30.0668, 79.0193],
    "Assam": [26.2006, 92.9376],
    "Amazon": [-3.4653, -62.2159],
    "Sundarbans": [21.9497, 89.1833],
    "Western Ghats": [10.8505, 76.2711]
}

map_data = pd.DataFrame({
    "lat": [region_coords[region][0]],
    "lon": [region_coords[region][1]]
})

st.map(map_data)

st.divider()

# =============================
# SIMULATE HIGH ALERT
# =============================
simulate_alert = st.button("🚨 Simulate High Alert (Demo Mode)")

if simulate_alert:

    st.session_state.blink = True
    st.session_state.total_scans += 1
    st.session_state.threats_detected += 1
    st.session_state.high_alerts += 1

    top_label = "Chainsaw"
    top_confidence = 0.92

    alert_entry = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Region": region,
        "Threat": top_label,
        "Confidence (%)": 92
    }
    st.session_state.alert_history.append(alert_entry)

    st.error(f"🚨 HIGH ALERT: {top_label} detected in {region}")

    # Siren
    st.markdown("""
    <audio autoplay>
        <source src="https://www.soundjay.com/misc/sounds/siren-01.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

    # Email Simulation
    st.info("📧 Email Notification Sent to Forest Control Authority (Simulated Azure Logic App)")

    # Confidence Dial
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=92,
        title={'text': "AI Confidence Level"},
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

# =============================
# PDF EXPORT
# =============================
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

if st.session_state.alert_history:
    st.divider()
    st.subheader("🗂 Alert History")
    history_df = pd.DataFrame(st.session_state.alert_history)
    st.dataframe(history_df, use_container_width=True)

    pdf_file = generate_pdf(history_df)
    st.download_button(
        label="📄 Download Alert Report (PDF)",
        data=pdf_file,
        file_name="alert_report.pdf",
        mime="application/pdf"
    )

st.info("Upload audio or use Demo Mode to simulate detection.")
