import streamlit as st
import numpy as np
import pandas as pd
import librosa
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

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
# UI
# =============================
st.title("🌱 Bio-Acoustic Sentinel")
st.markdown("AI-powered Real-Time Environmental Threat Detection System")

st.sidebar.header("🛠 System Controls")
sensitivity = st.sidebar.slider("Detection Sensitivity", 0, 100, 75)
st.sidebar.success("🟢 System Status: ACTIVE")

st.divider()

uploaded_file = st.file_uploader("Upload forest audio (.wav/.mp3)", type=["wav", "mp3"])

# =============================
# Audio Processing
# =============================
if uploaded_file is not None:

    st.audio(uploaded_file)

    # Load audio
    waveform, sr = librosa.load(uploaded_file, sr=16000)

    # =============================
    # Lightweight AI Simulation
    # =============================
    energy = np.mean(np.abs(waveform))

    # Simulated AI classification logic
    if energy > 0.15:
        top_label = "Chainsaw"
        top_confidence = np.random.uniform(0.75, 0.95)
    elif energy > 0.10:
        top_label = "Gunshot"
        top_confidence = np.random.uniform(0.65, 0.85)
    elif energy > 0.07:
        top_label = "Fire Crackling"
        top_confidence = np.random.uniform(0.60, 0.80)
    else:
        top_label = "Forest Ambient"
        top_confidence = np.random.uniform(0.80, 0.95)

    st.subheader("🔍 AI Detection Result")

    # =============================
    # Threat Logic
    # =============================
    is_threat = any(keyword.lower() in top_label.lower() for keyword in THREAT_KEYWORDS)

    if is_threat and top_confidence > CONFIDENCE_THRESHOLD:
        st.error(f"🚨 ALERT: {top_label}")
        st.warning(f"Confidence: {round(top_confidence * 100, 2)}%")

        if top_confidence > 0.85:
            st.error("⚠ Escalation Level: HIGH")
        else:
            st.warning("⚠ Escalation Level: MEDIUM")

    else:
        st.success("✅ No Critical Threat Detected")
        st.info(f"Top Sound: {top_label}")
        st.write(f"Confidence: {round(top_confidence * 100, 2)}%")

    # =============================
    # Event Log
    # =============================
    log_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Detected Label": [top_label],
        "Confidence (%)": [round(top_confidence * 100, 2)],
        "Threat Detected": [is_threat]
    }

    df = pd.DataFrame(log_data)
    st.subheader("📋 Detection Log")
    st.dataframe(df, use_container_width=True)

    # =============================
    # Waveform Visualization
    # =============================
    st.subheader("📈 Audio Waveform")

    fig, ax = plt.subplots()
    ax.plot(waveform[:5000])
    ax.set_title("Audio Signal Snapshot")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitude")
    st.pyplot(fig)

    # =============================
    # Confidence Distribution
    # =============================
    st.subheader("📊 Confidence Distribution")
    fake_scores = np.random.rand(20)
    st.line_chart(fake_scores)

else:
    st.info("Upload an audio file to begin detection.")
