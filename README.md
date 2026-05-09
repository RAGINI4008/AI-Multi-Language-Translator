# AI-Multi-Language-Translator
AI-powered multi-language translator with auto language detection, instant translation, MP3 audio output, translation history, and a modern dark UI built using Streamlit..
title: AI Translator
sdk: streamlit
app_file: app.py
python_version: "3.10"
---
# AI-Powered Multi-Language Translator with Voice-to-Voice Translation

A complete working AI-powered multilingual translator web application using Python and open-source technologies.

## Features

*   **Text translation:** Translate text between multiple languages.
*   **Voice-to-text translation:** Speak into the microphone and get translated text.
*   **Voice-to-voice translation:** Speak into the microphone, get translated text, and hear the translated audio playback.
*   **Automatic language detection:** The system detects the input language automatically from text.
*   **Auto Audio Playback:** Translated speech automatically plays back.
*   **Translation History:** Keeps track of translations during the session.

## Supported Languages

*   English
*   Hindi
*   Marathi
*   Tamil
*   Telugu
*   Bengali
*   Gujarati
*   Kannada
*   Malayalam
*   Punjabi
*   Urdu
*   Spanish
*   French
*   German

## Technology Stack

*   **Frontend:** Streamlit
*   **Speech Recognition (Voice-to-Text):** OpenAI Whisper
*   **Translation Model:** Hugging Face Transformers (`facebook/nllb-200-distilled-600M`)
*   **Text-to-Speech:** gTTS (primary/fallback)
*   **Language Detection:** `langdetect`
*   **Audio processing:** `sounddevice`, `pydub`

## Installation

1.  **Clone the repository or navigate to the project directory:**
    ```bash
    cd c:\ai_tran\ai_translator
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On Linux/macOS
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Depending on your OS, you might need to install `ffmpeg` for `pydub` and Whisper to work correctly with audio files. On Windows, download the binaries and add them to your PATH. On Ubuntu: `sudo apt install ffmpeg`.*

## Running the Application

1.  **Start the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
2.  Open your browser to the URL provided (usually `http://localhost:8501`).
    *Note: The first time you run a translation or transcribe audio, the models (NLLB, Whisper) will be downloaded from Hugging Face which might take some time and disk space depending on your internet connection.*

