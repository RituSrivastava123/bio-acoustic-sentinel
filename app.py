import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

# ===== HEADER =====
st.title("🌱 Bio-Acoustic Sentinel")
st.markdown("AI-powered Real-Time Environmental Threat Detection System")

st.divider()

# ===== SIDEBAR =====
st.sidebar.header("🛠 System Controls")
sensitivity = st.sidebar.slider("Detection Sensitivity", 0, 100, 75)
st.sidebar.write("Current Sensitivity:", sensitivity)

st.sidebar.divider()
st.sidebar.success("🟢 System Status: ACTIVE")

# ===== MAIN SECTION =====
st.subheader("📂 Upload Forest Audio")

uploaded_file = st.file_uploader("Upload an audio file (.wav or .mp3)", type=["wav", "mp3"])

if uploaded_file is not None:

    st.audio(uploaded_file)

    st.subheader("🔍 Running AI Analysis...")
    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # Simulated Threat Types
    threats = ["Chainsaw Activity", "Gunshot Sound", "Forest Fire Crackle", "Normal Forest Ambience"]
    detected_threat = random.choice(threats)
    confidence = random.randint(70, 99)

    st.divider()

    # Threat Logic
    if detected_threat != "Normal Forest Ambience":
        st.error(f"🚨 ALERT: {detected_threat}")
        st.warning(f"Confidence Level: {confidence}%")

        if confidence > 90:
            st.error("⚠ Escalation Level: HIGH — Immediate Action Required")
        else:
            st.warning("⚠ Escalation Level: MEDIUM — Monitor Situation")

    else:
        st.success("✅ No Threat Detected")
        st.info(f"Confidence Level: {confidence}%")

    # ===== EVENT LOG =====
    st.subheader("📋 Detection Log")

    log_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Detected Event": [detected_threat],
        "Confidence (%)": [confidence],
        "Sensitivity Setting": [sensitivity]
    }

    df = pd.DataFrame(log_data)
    st.dataframe(df, use_container_width=True)

    # ===== CONFIDENCE GRAPH =====
    st.subheader("📊 Confidence Trend")
    st.line_chart([random.randint(60, 100) for _ in range(20)])

else:
    st.info("Please upload an audio file to start analysis.")
