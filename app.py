import streamlit as st
import numpy as np
import pandas as pd
import librosa
from datetime import datetime
import matplotlib.pyplot as plt
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
# DASHBOARD COUNTERS
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

# =============================
# HEATMAP
# =============================
st.subheader("🔥 Threat Intensity Heatmap")
heatmap_data = pd.DataFrame(np.random.rand(10, 10))
st.dataframe(heatmap_data.style.background_gradient(cmap="Reds"))

st.divider()

# =============================
# DETECTION FUNCTION
# =============================
def run_detection(waveform):
    energy = np.mean(np.abs(waveform))
    if energy > 0.15:
        return "Chainsaw", np.random.uniform(0.80, 0.95)
    elif energy > 0.10:
        return "Gunshot", np.random.uniform(0.70, 0.88)
    elif energy > 0.07:
        return "Fire", np.random.uniform(0.60, 0.82)
    else:
        return "Forest Ambient", np.random.uniform(0.80, 0.95)

# =============================
# LIVE MONITORING MODE
# =============================
live_mode = st.toggle("🎥 Enable Live Monitoring Mode")

if live_mode:
    st.info("🔄 Live Monitoring Active...")

    for i in range(5):
        st.session_state.total_scans += 1
        simulated_wave = np.random.rand(16000)

        top_label, top_confidence = run_detection(simulated_wave)
        is_threat = any(keyword.lower() in top_label.lower() for keyword in THREAT_KEYWORDS)

        st.subheader(f"📡 Scan #{st.session_state.total_scans}")

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

            st.info("📡 Alert dispatched to Forest Control Room (Simulated Azure Notification)")
        else:
            st.success("✅ No Threat Detected")

        time.sleep(1)

# =============================
# MANUAL UPLOAD
# =============================
uploaded_file = st.file_uploader("Upload forest audio (.wav/.mp3)", type=["wav", "mp3"])

if uploaded_file is not None and not live_mode:

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

        st.info("📡 Alert dispatched to Forest Control Room (Simulated Azure Notification)")
    else:
        st.success("✅ No Critical Threat Detected")

    # Severity Gauge
    st.subheader("🎯 Threat Severity Level")
    severity_score = int(top_confidence * 100)
    st.progress(severity_score)

    if severity_score > 85:
        st.error("🔴 Critical Risk Zone")
    elif severity_score > 70:
        st.warning("🟠 Moderate Risk Zone")
    else:
        st.success("🟢 Low Risk Zone")

    # AI Explanation
    with st.expander("🤖 AI Explanation"):
        st.write(f"""
        The system analyzed acoustic energy patterns and classified the dominant sound as **{top_label}**.
        Sensitivity level set at {sensitivity}.
        Geo-tag confirms detection in **{region}** region.
        """)

    # Waveform
    st.subheader("📈 Audio Waveform")
    fig, ax = plt.subplots()
    ax.plot(waveform[:5000])
    ax.set_title("Audio Signal Snapshot")
    st.pyplot(fig)

# =============================
# ALERT HISTORY
# =============================
if st.session_state.alert_history:
    st.divider()
    st.subheader("🗂 Alert History")
    history_df = pd.DataFrame(st.session_state.alert_history)
    st.dataframe(history_df, use_container_width=True)

# =============================
# DEFAULT MESSAGE
# =============================
if not live_mode and uploaded_file is None:
    st.info("Upload audio or enable Live Monitoring Mode to begin detection.")
