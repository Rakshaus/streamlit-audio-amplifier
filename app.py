import streamlit as st
from pydub import AudioSegment
import os
import tempfile

# Title
st.title("🔊 Audio Amplifier Web App")

# File upload
uploaded_file = st.file_uploader("📁 Upload an audio file", type=["wav", "mp3", "ogg"])

# dB Gain input
gain_db = st.slider("🎚️ Select Amplification Level (in dB)", min_value=1, max_value=100, value=10)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    # Read audio into pydub format
    audio = AudioSegment.from_file(uploaded_file)

    # Amplify the audio
    amplified_audio = audio + gain_db

    # Export to a temp file
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    amplified_audio.export(temp_output.name, format="wav")

    # Playback
    st.audio(temp_output.name, format="audio/wav")

    # Download button
    with open(temp_output.name, "rb") as f:
        st.download_button(
            label="⬇️ Download Amplified Audio",
            data=f,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_amplified.wav",
            mime="audio/wav"
        )

    st.success("✅ Audio amplified successfully!")

else:
    st.info("Upload an audio file to get started.")
