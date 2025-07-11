import streamlit as st
from pydub import AudioSegment
import os
import tempfile

# Title and Description
st.title("🔊 Audio Amplifier Web App")
st.markdown("Upload an audio file, choose a volume gain (in decibels), and download the amplified version.")

# File uploader
uploaded_file = st.file_uploader("📁 Upload an audio file", type=["wav", "mp3", "ogg"])

# Amplification level (dB)
gain_db = st.slider("🎚️ Amplification Level (dB)", min_value=1, max_value=100, value=10)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    # Convert uploaded file into a Pydub AudioSegment
    audio = AudioSegment.from_file(uploaded_file)

    # Apply gain
    amplified_audio = audio + gain_db

    # Save to temporary file
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    amplified_audio.export(temp_output.name, format="wav")

    # Audio preview
    st.audio(temp_output.name, format="audio/wav")

    # Download button
    with open(temp_output.name, "rb") as f:
        st.download_button(
            label="⬇️ Download Amplified Audio",
            data=f.read(),
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_amplified.wav",
            mime="audio/wav"
        )

    st.success("✅ Audio amplified successfully!")
else:
    st.info("👆 Please upload an audio file to begin.")
