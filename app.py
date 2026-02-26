import streamlit as st
import numpy as np
import pandas as pd
import librosa
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

# =============================
# DARK CYBER THEME
# =============================
st.markdown("""
<style>
body { background-color: #0e1117; }
.stApp { background-color: #0e1117; color: white; }
h1, h2, h3 { color: #00ffcc; }
[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
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

# =============================
# CONFIG
# =============================
THREAT_KEYWORDS = ["Chainsaw", "Gunshot", "Explosion", "Fire", "Siren"]
CONFIDENCE_THRESHOLD = 0.6

# =============================
# HEADER
# =============================
st.title("🌱 Bio-Acoustic Sentinel")
st.markdown("☁ Powered by Microsoft Azure AI Infrastructure (Simulation)")
st.markdown("AI-powered Real-Time Environmental Threat Detection System")

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
# SIMULATE HIGH ALERT BUTTON
# =============================
simulate_alert = st.button("🚨 Simulate High Alert (Demo Mode)")

if simulate_alert:

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

    st.subheader("🔍 AI Detection Result")
    st.error(f"🚨 HIGH ALERT: {top_label} detected in {region}")

    # 🔊 Siren Sound
    st.markdown("""
    <audio autoplay>
        <source src="https://www.soundjay.com/misc/sounds/siren-01.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

    # 📧 Email Simulation
    st.info("📧 Email Notification Sent to Forest Control Authority (Simulated Azure Logic App)")

    # 🎯 AI Confidence Dial
    st.subheader("🎯 AI Confidence Dial")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=92,
        title={'text': "Confidence Level"},
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
# AUDIO UPLOAD DETECTION
# =============================
uploaded_file = st.file_uploader("Upload forest audio (.wav/.mp3)", type=["wav", "mp3"])

def run_detection(waveform):
    energy = np.mean(np.abs(waveform))
    if energy > 0.15:
        return "Chainsaw", np.random.uniform(0.85, 0.95)
    elif energy > 0.10:
        return "Gunshot", np.random.uniform(0.70, 0.88)
    elif energy > 0.07:
        return "Fire", np.random.uniform(0.60, 0.82)
    else:
        return "Forest Ambient", np.random.uniform(0.80, 0.95)

if uploaded_file is not None:

    st.audio(uploaded_file)
    waveform, sr = librosa.load(uploaded_file, sr=16000)

    st.session_state.total_scans += 1
    top_label, top_confidence = run_detection(waveform)
    is_threat = any(keyword.lower() in top_label.lower() for keyword in THREAT_KEYWORDS)

    st.subheader("🔍 AI Detection Result")

    if is_threat and top_confidence > CONFIDENCE_THRESHOLD:
        st.session_state.threats_detected += 1

        alert_entry = {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Region": region,
            "Threat": top_label,
            "Confidence (%)": round(top_confidence*100, 2)
        }
        st.session_state.alert_history.append(alert_entry)

        if top_confidence > 0.85:
            st.session_state.high_alerts += 1
            st.error(f"🚨 HIGH ALERT: {top_label} detected in {region}")
        else:
            st.warning(f"⚠ MEDIUM ALERT: {top_label} detected in {region}")

    else:
        st.success("✅ No Critical Threat Detected")

    # Waveform
    st.subheader("📈 Audio Waveform")
    fig2, ax = plt.subplots()
    ax.plot(waveform[:5000])
    ax.set_title("Audio Signal Snapshot")
    st.pyplot(fig2)

# =============================
# ALERT HISTORY
# =============================
if st.session_state.alert_history:
    st.divider()
    st.subheader("🗂 Alert History")
    history_df = pd.DataFrame(st.session_state.alert_history)
    st.dataframe(history_df, use_container_width=True)

if uploaded_file is None and not simulate_alert:
    st.info("Upload audio or use Demo Mode to simulate detection.")
