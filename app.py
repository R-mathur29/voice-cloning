import os
os.environ["COQUI_TOS_AGREED"] = "1"  # Important: Required for XTTS v2 license

import streamlit as st
import os
import uuid
import numpy as np
from TTS.api import TTS
from resemblyzer import VoiceEncoder, preprocess_wav

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

AUDIO_DIR = "preprocessed_audio"
OUTPUT_DIR = "output_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

speakers = sorted(os.listdir(AUDIO_DIR))

st.title("🗣️ Voice Cloning with XTTS")
selected_speaker = st.selectbox("Choose a speaker", speakers)
input_text = st.text_area("Enter the text to synthesize")

if st.button("Generate Speech"):
    speaker_dir = os.path.join(AUDIO_DIR, selected_speaker)
    wav_file = next((f for f in os.listdir(speaker_dir) if f.endswith(".wav")), None)
    
    if wav_file:
        speaker_wav = os.path.join(speaker_dir, wav_file)
        output_filename = f"{uuid.uuid4().hex}.wav"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        tts.tts_to_file(
            text=input_text,
            speaker_wav=speaker_wav,
            language="en",
            file_path=output_path
        )

        st.audio(output_path, format="audio/wav")
    else:
        st.error("No .wav file found for selected speaker.")
