"""
translator.py
Handles translation logic using a multilingual Hugging Face model.

Important:
- We load the model lazily so importing this module never crashes the app.
- On first run, the model download can take time and requires internet access.
"""

from __future__ import annotations

import os
from huggingface_hub import snapshot_download
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from utils import get_gtts_code, get_nllb_code

# Offline model (smaller than NLLB; still multilingual).
# M2M100 uses ISO-like language codes such as "en", "hi", "fr", etc.
MODEL_NAME = "facebook/m2m100_418M"

# Determine device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_tokenizer = None
_model = None

_LOCAL_MODEL_DIR = os.path.join(os.path.dirname(__file__), "hf_models", "facebook--m2m100-418M")


def _load_model():
    global _tokenizer, _model
    if _tokenizer is not None and _model is not None:
        return _tokenizer, _model

    try:
        print(f"Loading Translation Model ({MODEL_NAME}). This may take a moment on first run...")
        # Some Windows setups fail to materialize Hugging Face cache snapshot files (symlink/hardlink issues).
        # Download the repo into a normal local directory with real files instead.
        os.makedirs(os.path.dirname(_LOCAL_MODEL_DIR), exist_ok=True)
        snapshot_download(
            repo_id=MODEL_NAME,
            local_dir=_LOCAL_MODEL_DIR,
            local_dir_use_symlinks=False,
            resume_download=True,
        )

        _tokenizer = AutoTokenizer.from_pretrained(_LOCAL_MODEL_DIR, local_files_only=True)
        _model = AutoModelForSeq2SeqLM.from_pretrained(_LOCAL_MODEL_DIR, local_files_only=True).to(DEVICE)
        print(f"Translation model loaded on {DEVICE}.")
        return _tokenizer, _model
    except Exception as e:
        raise RuntimeError(
            "Failed to load the translation model. This usually happens when the Hugging Face "
            "download/cache is incomplete or the machine is offline. "
            "Try: (1) ensure internet access, (2) delete the cached folder for this model, "
            "then rerun the app.\n\n"
            f"Original error: {e}"
        ) from e


def _translate_online(text: str, source_language: str, target_language: str) -> str:
    # Online fallback (fast start; requires internet).
    # Uses language codes compatible with Google Translate (same as gTTS codes for our supported set).
    from deep_translator import GoogleTranslator

    src = get_gtts_code(source_language)
    tgt = get_gtts_code(target_language)
    if src == tgt:
        return text

    return GoogleTranslator(source=src, target=tgt).translate(text)


def translate_text(text, source_language, target_language):
    """
    Translates text from source_language to target_language using NLLB-200.

    Args:
        text (str): Text to translate.
        source_language (str): Human-readable source language name (e.g. 'English').
        target_language (str): Human-readable target language name (e.g. 'Hindi').

    Returns:
        str: Translated text, or an error message string.
    """
    try:
        if not text or not text.strip():
            return ""

        backend = os.environ.get("TRANSLATION_BACKEND", "auto").strip().lower()

        # Fast path: online translation (no big model download).
        if backend == "online":
            return _translate_online(text, source_language, target_language)

        # Offline model uses Google-like language codes (same codes we already maintain for gTTS)
        src_code = get_gtts_code(source_language)
        tgt_code = get_gtts_code(target_language)
        if src_code == tgt_code:
            return text

        # Auto mode: try online first for instant UX; fall back to offline model if online fails.
        if backend == "auto":
            try:
                return _translate_online(text, source_language, target_language)
            except Exception:
                pass

        tokenizer, model = _load_model()

        # M2M100: set source language, and force target language token at generation start.
        tokenizer.src_lang = src_code
        encoded = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(DEVICE)

        forced_bos_token_id = tokenizer.get_lang_id(tgt_code)

        # Generate translation
        generated_tokens = model.generate(
            **encoded,
            forced_bos_token_id=forced_bos_token_id,
            max_length=512
        )

        # Decode translated tokens
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translated_text

    except Exception as e:
        error_msg = f"Translation error: {e}"
        print(error_msg)
        return error_msg
