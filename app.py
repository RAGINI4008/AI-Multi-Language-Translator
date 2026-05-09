# app.py
# Main Streamlit UI and application workflow.
import streamlit as st
print(st.__version__)
import streamlit as st
import os
import tempfile
import numpy as np


# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Multi-Language Translator",
    page_icon="🌐",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* PREMIUM RUBY CRIMSON BACKGROUND */
    .stApp {
        background: radial-gradient(circle at 0% 0%, rgba(225, 29, 72, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 100% 100%, rgba(244, 63, 94, 0.08) 0%, transparent 50%),
                    #1c050b;
        color: #f8fafc;
    }

    /* HERO HEADER */
    .hero-header {
        text-align: center;
        padding: 3rem 1rem 2rem;
    }

    .hero-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #fda4af 50%, #e11d48 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .hero-header p {
        color: #94a3b8;
        font-size: 1.15rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }

    /* PREMIUM GLASS CARD */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.2);
    }

    /* SECTION LABELS */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #f43f5e;
        margin-bottom: 0.75rem;
        opacity: 0.9;
    }

    /* LANGUAGE BADGE */
    .lang-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        border: 1px solid rgba(244, 63, 94, 0.2);
        border-radius: 12px;
        padding: 0.4rem 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* TRANSLATED BOX */
    .translated-box {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        font-size: 1.15rem;
        line-height: 1.6;
        color: #f1f5f9;
        min-height: 100px;
        white-space: pre-wrap;
    }

    /* HISTORY ENTRY */
    .history-entry {
        background: rgba(255, 255, 255, 0.02);
        border-left: 4px solid #f43f5e;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 0.8rem;
    }

    .history-entry .meta {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    /* PREMIUM BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #f43f5e 0%, #9f1239 100%);
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(159, 18, 57, 0.3) !important;
        filter: brightness(1.1);
    }

    /* TEXT AREA */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f1f5f9 !important;
        border-radius: 14px !important;
        padding: 0.5rem !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(244, 63, 94, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Lazy Module Loading (cached so models load once) ──────────────────────────
@st.cache_resource(show_spinner="🔄 Loading translation model (first run may take a few minutes)...")
def load_translator():
    from translator import translate_text
    return translate_text

@st.cache_resource(show_spinner="🎙️ Loading speech recognition model...")
def load_stt():
    import speech_to_text as stt_module
    return stt_module

@st.cache_resource
def load_tts():
    from text_to_speech import text_to_speech, cleanup_audio_file
    return text_to_speech, cleanup_audio_file

# Import lightweight modules
from language_detection import detect_language
from utils import SUPPORTED_LANGUAGES

# ── Session State ─────────────────────────────────────────────────────────────
if "translation_history" not in st.session_state:
    st.session_state.translation_history = []
if "last_audio_path" not in st.session_state:
    st.session_state.last_audio_path = None

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>🌐 AI Multi-Language Translator</h1>
    <p>Voice-to-Voice · Text Translation · Auto Language Detection · 14 Languages</p>
</div>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1], gap="large")

# ───────────────────── LEFT COLUMN – Input ─────────────────────────────
with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # === Translation engine selector ===
    st.markdown('<p class="section-label">Translation Engine</p>', unsafe_allow_html=True)
    engine = st.selectbox(
        label="Translation Engine",
        options=["Fast (Online)", "Offline (Small AI Model)"],
        index=0,
        label_visibility="collapsed",
        key="translation_engine_select",
        help="Fast uses online translate (no large downloads). Offline uses a smaller multilingual AI model (first download, then works offline).",
    )
    os.environ["TRANSLATION_BACKEND"] = "online" if engine.startswith("Fast") else "offline"

    # === Target language selector ===
    st.markdown('<p class="section-label">Target Language</p>', unsafe_allow_html=True)
    target_language = st.selectbox(
        label="Target Language",
        options=SUPPORTED_LANGUAGES,
        index=1,          # default: Hindi
        label_visibility="collapsed",
        key="target_lang_select"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # === Input Mode Tabs ===
    tab_text, tab_voice = st.tabs(["✏️ Text Input", "🎙️ Voice Input"])

    # ── TEXT INPUT TAB ──
    with tab_text:
        st.markdown('<p class="section-label">Enter text to translate</p>', unsafe_allow_html=True)
        user_text = st.text_area(
            label="Input Text",
            placeholder="Type your text here...",
            height=160,
            label_visibility="collapsed",
            key="text_input_area"
        )

        if st.button("🌐 Translate Text", use_container_width=True, key="translate_text_btn"):
            if user_text.strip():
                with st.spinner("Detecting language & translating..."):
                    translate_fn = load_translator()
                    detected_lang = detect_language(user_text)
                    translated = translate_fn(user_text, detected_lang, target_language)

                st.session_state.detected_lang = detected_lang
                st.session_state.translated_text = translated
                st.session_state.input_text_display = user_text

                # Add to history
                st.session_state.translation_history.insert(0, {
                    "input": user_text,
                    "output": translated,
                    "src_lang": detected_lang,
                    "tgt_lang": target_language
                })
            else:
                st.warning("Please enter some text to translate.")

    # ── VOICE INPUT TAB ──
    with tab_voice:
        st.info("Upload audio file (wav/mp3)")

        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

        if audio_file is not None:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

            with open(tmp.name, "wb") as f:
                f.write(audio_file.read())

            stt = load_stt()
            text, err = stt.transcribe_audio(tmp.name)

            os.remove(tmp.name)

            if text:
                translate_fn = load_translator()
                detected = detect_language(text)
                result = translate_fn(text, detected, target_language)

                st.session_state.result = result
                st.session_state.input = text
                st.session_state.detected = detected
            else:
                st.error("Transcription failed")


# ────────────────────── RIGHT COLUMN – Output ─────────────────────────────
with col_output:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown('<p class="section-label">Translation Output</p>', unsafe_allow_html=True)

    detected_lang = st.session_state.get("detected_lang", None)
    translated_text = st.session_state.get("translated_text", None)
    input_text_display = st.session_state.get("input_text_display", None)

    if detected_lang:
        st.markdown(
            f'<span class="lang-badge">🔍 Detected: {detected_lang} → {target_language}</span>',
            unsafe_allow_html=True
        )

    if input_text_display:
        st.markdown('<p class="section-label" style="margin-top:0.8rem">Original Text</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="translated-box" style="color:#c7d2fe">{input_text_display}</div>', unsafe_allow_html=True)

    st.markdown('<p class="section-label" style="margin-top:0.8rem">Translated Text</p>', unsafe_allow_html=True)
    if translated_text:
        st.markdown(f'<div class="translated-box">{translated_text}</div>', unsafe_allow_html=True)

        # ── Audio Playback ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">🔊 Audio Playback</p>', unsafe_allow_html=True)

        if st.button("🔊 Generate & Play Audio", use_container_width=True, key="tts_btn"):
            with st.spinner("Generating speech..."):
                tts_fn, cleanup_fn = load_tts()
                audio_path = tts_fn(translated_text, target_language)

            if audio_path:
                # Cleanup previous temp file
                if st.session_state.last_audio_path:
                    cleanup_fn(st.session_state.last_audio_path)
                st.session_state.last_audio_path = audio_path

                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                # Autoplay audio
                import base64
                audio_b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(
                    f'<audio autoplay controls style="width:100%;border-radius:10px;margin-top:0.5rem">'
                    f'<source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">'
                    f'</audio>',
                    unsafe_allow_html=True
                )
            else:
                st.error("Failed to generate audio. Please check your internet connection (gTTS requires internet).")
    else:
        st.markdown('<div class="translated-box" style="color:#4a5568;font-style:italic">Translation will appear here...</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Translation History ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<p class="section-label">📜 Translation History (This Session)</p>', unsafe_allow_html=True)

history = st.session_state.translation_history
if not history:
    st.markdown('<p style="color:#4a5568;font-style:italic;font-size:0.9rem">No translations yet. Start translating above!</p>', unsafe_allow_html=True)
else:
    cols = st.columns([1, 5])
    with cols[1]:
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.translation_history = []
            st.rerun()

    for i, entry in enumerate(history[:10]):  # Show latest 10
        st.markdown(f"""
        <div class="history-entry">
            <div class="meta">#{i+1} · {entry['src_lang']} → {entry['tgt_lang']}</div>
            <div><strong>In:</strong> {entry['input'][:120]}{'...' if len(entry['input']) > 120 else ''}</div>
            <div style="color:#fda4af"><strong>Out:</strong> {entry['output'][:120]}{'...' if len(entry['output']) > 120 else ''}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
