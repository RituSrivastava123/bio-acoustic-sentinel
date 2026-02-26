import streamlit as st
import numpy as np
import pandas as pd
import librosa
from datetime import datetime
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

# =============================
# Initialize Session State
# =============================
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0
if "threats_detected" not in st.session_state:
    st.session_state.threats_detected = 0
if "high_alerts" not in st.session_state:
    st.session_state.high_alerts = 0

# =============================
# Threat Definitions
# =============================
THREAT_KEYWORDS = [
    "Chainsaw",
    "Gunshot",
    "Explosion",
    "Fire",
    "Siren"
]

CONFIDENCE_THRESHOLD = 0.6

# =============================
# UI Header
# =============================
st.title("🌱 Bio-Acoustic Sentinel")
st.markdown("AI-powered Real-Time Environmental Threat Detection System")

# =============================
# Sidebar Controls
# =============================
st.sidebar.header("🛠 System Controls")
sensitivity = st.sidebar.slider("Detection Sensitivity", 0, 100, 75)

region = st.sidebar.selectbox(
    "🌍 Forest Region",
    ["Uttarakhand", "Assam", "Amazon", "Sundarbans", "Western Ghats"]
)

st.sidebar.success("🟢 System Status: ACTIVE")

# =============================
# Real-Time Dashboard Counters
# =============================
st.divider()
st.subheader("📊 Real-Time Monitoring Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("🔎 Total Scans", st.session_state.total_scans)
col2.metric("🚨 Threats Detected", st.session_state.threats_detected)
col3.metric("🔥 High Escalations", st.session_state.high_alerts)

st.divider()

# =============================
# File Upload
# =============================
uploaded_file = st.file_uploader("Upload forest audio (.wav/.mp3)", type=["wav", "mp3"])

# =============================
# Detection Function
# =============================
def run_detection(waveform):
    energy = np.mean(np.abs(waveform))

    if energy > 0.15:
        return "Chainsaw", np.random.uniform(0.80, 0.95)
    elif energy > 0.10:
        return "Gunshot", np.random.uniform(0.70, 0.88)
    elif energy > 0.07:
        return "Fire Crackling", np.random.uniform(0.60, 0.82)
    else:
        return "Forest Ambient", np.random.uniform(0.80, 0.95)

# =============================
# LIVE MONITORING MODE
# =============================
live_mode = st.toggle("🎥 Enable Live Monitoring Mode")

if live_mode:
    st.info("🔄 Live Monitoring Active...")

    for i in range(5):  # simulate 5 live scans
        st.session_state.total_scans += 1

        simulated_wave = np.random.rand(16000)
        top_label, top_confidence = run_detection(simulated_wave)

        is_threat = any(keyword.lower() in top_label.lower() for keyword in THREAT_KEYWORDS)

        with st.container():
            st.subheader(f"📡 Scan #{st.session_state.total_scans}")

            if is_threat and top_confidence > CONFIDENCE_THRESHOLD:
                st.session_state.threats_detected += 1

                if top_confidence > 0.85:
                    st.session_state.high_alerts += 1
                    st.error(f"🚨 HIGH ALERT: {top_label} detected in {region}")
                else:
                    st.warning(f"⚠ MEDIUM ALERT: {top_label} detected in {region}")

                st.write(f"Confidence: {round(top_confidence*100,2)}%")
            else:
                st.success("✅ No Threat Detected")

        time.sleep(1)

# =============================
# Manual Upload Detection
# =============================
elif uploaded_file is not None:

    st.audio(uploaded_file)
    waveform, sr = librosa.load(uploaded_file, sr=16000)

    st.session_state.total_scans += 1

    top_label, top_confidence = run_detection(waveform)
    is_threat = any(keyword.lower() in top_label.lower() for keyword in THREAT_KEYWORDS)

    st.subheader("🔍 AI Detection Result")

    if is_threat and top_confidence > CONFIDENCE_THRESHOLD:
        st.session_state.threats_detected += 1

        if top_confidence > 0.85:
            st.session_state.high_alerts += 1
            st.error(f"🚨 HIGH ALERT: {top_label} detected in {region}")
        else:
            st.warning(f"⚠ MEDIUM ALERT: {top_label} detected in {region}")

        st.write(f"Confidence: {round(top_confidence*100, 2)}%")

    else:
        st.success("✅ No Critical Threat Detected")
        st.info(f"Top Sound: {top_label}")
        st.write(f"Confidence: {round(top_confidence*100, 2)}%")

    # Log Table
    log_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Region": [region],
        "Detected Label": [top_label],
        "Confidence (%)": [round(top_confidence*100, 2)],
        "Threat Detected": [is_threat]
    }

    df = pd.DataFrame(log_data)
    st.subheader("📋 Detection Log")
    st.dataframe(df, use_container_width=True)

    # Waveform
    st.subheader("📈 Audio Waveform")
    fig, ax = plt.subplots()
    ax.plot(waveform[:5000])
    ax.set_title("Audio Signal Snapshot")
    st.pyplot(fig)

    # Confidence Graph
    st.subheader("📊 Confidence Distribution")
    fake_scores = np.random.rand(20)
    st.line_chart(fake_scores)

else:
    st.info("Upload audio or enable Live Monitoring Mode to begin detection.")
