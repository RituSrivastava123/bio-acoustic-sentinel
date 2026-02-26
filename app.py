import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import librosa
from datetime import datetime

st.set_page_config(page_title="Bio-Acoustic Sentinel", layout="wide")

# =============================
# Load YAMNet Model
# =============================
@st.cache_resource
def load_model():
    return hub.load("https://tfhub.dev/google/yamnet/1")

model = load_model()

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

    # Run YAMNet
    scores, embeddings, spectrogram = model(waveform)

    scores_np = scores.numpy()
    mean_scores = np.mean(scores_np, axis=0)

    # Load YAMNet class names
    class_map_path = model.class_map_path().numpy().decode("utf-8")
    class_names = pd.read_csv(class_map_path)["display_name"].tolist()

    # Get top prediction
    top_index = np.argmax(mean_scores)
    top_label = class_names[top_index]
    top_confidence = mean_scores[top_index]

    st.subheader("🔍 AI Detection Result")

    # =============================
    # Threat Logic
    # =============================
    is_threat = any(keyword.lower() in top_label.lower() for keyword in THREAT_KEYWORDS)

    if is_threat and top_confidence > CONFIDENCE_THRESHOLD:
        st.error(f"🚨 ALERT: {top_label}")
        st.warning(f"Confidence: {round(top_confidence*100, 2)}%")

        if top_confidence > 0.85:
            st.error("⚠ Escalation Level: HIGH")
        else:
            st.warning("⚠ Escalation Level: MEDIUM")

    else:
        st.success(f"✅ No Critical Threat Detected")
        st.info(f"Top Sound: {top_label}")
        st.write(f"Confidence: {round(top_confidence*100, 2)}%")

    # =============================
    # Event Log
    # =============================
    log_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Detected Label": [top_label],
        "Confidence (%)": [round(top_confidence*100, 2)],
        "Threat Detected": [is_threat]
    }

    df = pd.DataFrame(log_data)
    st.subheader("📋 Detection Log")
    st.dataframe(df, use_container_width=True)

    # Confidence Graph
    st.subheader("📊 Confidence Distribution")
    st.line_chart(mean_scores[:20])

else:
    st.info("Upload an audio file to begin detection.")
