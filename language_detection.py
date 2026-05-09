# language_detection.py
# Uses `langdetect` to identify the source language of a given text.

from langdetect import detect, DetectorFactory
from utils import LANGDETECT_TO_LANGUAGE

# Ensure consistent deterministic results
DetectorFactory.seed = 0

def detect_language(text):
    """
    Detects the language of the provided text.
    Returns the human-readable language name if supported, else defaults to English.
    """
    try:
        if not text or len(text.strip()) == 0:
            return "English"
        
        lang_code = detect(text)
        
        # Maps the langdetect code back to our application's language names (e.g., 'en' -> 'English')
        readable_language = LANGDETECT_TO_LANGUAGE.get(lang_code, "English")
        return readable_language
    except Exception as e:
        print(f"Error in language detection: {e}")
        # Default back to English upon failure
        return "English"
