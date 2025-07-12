import streamlit as st
from pydub import AudioSegment
import tempfile
import os
import pygame

# Function to amplify audio
def amplify_audio(input_audio, gain_db=10):
    # Convert to AudioSegment and apply amplification
    audio = AudioSegment.from_file(input_audio)
    amplified = audio + gain_db

    # Save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as out_file:
        amplified.export(out_file.name, format="wav")
        return out_file.name

# Streamlit UI
st.title("🎚️ Audio Amplifier Web App")
st.markdown("Upload an audio file, choose amplification level (in dB), and download the louder version.")

# Upload
uploaded_file = st.file_uploader("📁 Upload Audio File", type=["mp3", "wav", "ogg"])

# Amplification slider
gain = st.slider("Select Gain (dB)", min_value=0, max_value=50, value=10)

# Show audio player
if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")
    if st.button("🔊 Amplify Audio"):
        # Save uploaded file to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name

        # Amplify the audio
        output_path = amplify_audio(temp_input_path, gain_db=gain)
        st.success("Audio amplified successfully!")

        # Play amplified audio
        st.audio(output_path, format="audio/wav")

        # Download button
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Download Amplified Audio", data=f, file_name="amplified_audio.wav", mime="audio/wav")

        # Cleanup
        os.remove(temp_input_path)
        os.remove(output_path)
