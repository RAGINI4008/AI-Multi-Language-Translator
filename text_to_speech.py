# text_to_speech.py
# Handles audio generation using gTTS (with optional Coqui TTS fallback).

import os
import tempfile
from gtts import gTTS
from utils import get_gtts_code


def text_to_speech(text, language_name):
    """
    Converts text to speech and saves it as an MP3 file.
    Uses gTTS (Google Text-to-Speech) which is free and requires internet.

    Args:
        text (str): Text to convert to speech.
        language_name (str): Human-readable language name (e.g., 'Hindi').

    Returns:
        str: Path to the generated MP3 file, or None on failure.
    """
    try:
        if not text or not text.strip():
            return None

        lang_code = get_gtts_code(language_name)

        # Create a temporary file to hold the audio
        tmp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".mp3", prefix="tts_output_"
        )
        tmp_path = tmp_file.name
        tmp_file.close()

        # Generate speech using gTTS
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(tmp_path)

        return tmp_path

    except Exception as e:
        print(f"gTTS error: {e}")
        return None


def cleanup_audio_file(file_path):
    """Safely removes a temporary audio file."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Could not remove temp audio file {file_path}: {e}")
