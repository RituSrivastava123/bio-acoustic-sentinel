import streamlit as st
import random
import time

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

# ===== HEADER =====
st.title("🌱 Bio-Acoustic Sentinel")
st.markdown("AI-powered Environmental Threat Detection System")

st.divider()

# ===== SIDEBAR =====
st.sidebar.header("System Controls")
sensitivity = st.sidebar.slider("Detection Sensitivity", 0, 100, 75)
st.sidebar.write("Current Sensitivity:", sensitivity)

# ===== FILE UPLOAD =====
st.subheader("📂 Upload Forest Audio")

uploaded_file = st.file_uploader("Upload an audio file (.wav or .mp3)", type=["wav", "mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    st.subheader("🔍 Running Analysis...")
    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # Fake AI Prediction (temporary)
    threat_detected = random.choice([True, False])
    confidence = random.randint(70, 99)

    st.divider()

    if threat_detected:
        st.error(f"🚨 Threat Detected! Confidence: {confidence}%")
    else:
        st.success(f"✅ No Threat Detected. Confidence: {confidence}%")

    # Simple Chart
    st.subheader("📊 Detection Confidence Graph")
    st.line_chart([random.randint(50, 100) for _ in range(20)])

else:
    st.info("Please upload an audio file to start analysis.")
