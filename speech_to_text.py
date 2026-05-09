# speech_to_text.py
# Handles Whisper speech recognition.

import os
import sys
import warnings

# ── Auto-add bundled FFmpeg to PATH so Whisper can decode audio ──────────────
# 1. Try to use imageio-ffmpeg if available
try:
    import imageio_ffmpeg
    _ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    _ffmpeg_dir = os.path.dirname(_ffmpeg_path)
    if _ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
except Exception as _e:
    print(f"[speech_to_text] imageio_ffmpeg not available: {_e}")

# 2. Check for local ffmpeg.exe in the current script's directory (ai_translator/)
_local_dir = os.path.dirname(os.path.abspath(__file__))
_local_ffmpeg = os.path.join(_local_dir, "ffmpeg.exe")
if os.path.exists(_local_ffmpeg):
    if _local_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _local_dir + os.pathsep + os.environ.get("PATH", "")
        print(f"[speech_to_text] Added local FFmpeg directory to PATH: {_local_dir}")
else:
    print(f"[speech_to_text] Local ffmpeg.exe not found in {_local_dir}")


# Suppress FP16 warnings from Whisper on CPU
warnings.filterwarnings("ignore", category=UserWarning)

# ── Lazy model loading ────────────────────────────────────────────────────────
_whisper_model = None

def _get_model():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        # Using 'tiny' model for much faster inference on CPU
        print("Loading Whisper model ('tiny')...")
        _whisper_model = whisper.load_model("tiny")
    return _whisper_model


def transcribe_audio(audio_file_path):
    """
    Transcribes audio from the given WAV file path to text.

    Returns:
        (str, None)  – transcribed text on success
        (None, str)  – (None, error_message) on failure
    """
    if not os.path.exists(audio_file_path):
        return None, f"Audio file not found at {audio_file_path}"
    
    file_size = os.path.getsize(audio_file_path)
    if file_size < 100:
        return None, f"Audio file is too small ({file_size} bytes). Possibly no sound recorded."

    try:
        model = _get_model()
        print(f"[speech_to_text] Transcribing {audio_file_path} ({file_size} bytes)...")
        result = model.transcribe(audio_file_path, fp16=False)
        text = result.get("text", "").strip()
        
        if not text:
            print("[speech_to_text] Warning: Transcription returned empty text.")
            return None, "No speech detected in the audio clip."
            
        print(f"[speech_to_text] Transcription success: '{text[:50]}...'")
        return text, None
    except Exception as e:
        error_msg = f"Whisper error: {str(e)}"
        print(f"[speech_to_text] {error_msg}")
        import traceback
        traceback.print_exc()
        return None, error_msg

