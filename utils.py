# utils.py
# Helper module containing language codes and properties for different libraries.

# Supported languages list
SUPPORTED_LANGUAGES = [
    "English",
    "Hindi",
    "Marathi",
    "Tamil",
    "Telugu",
    "Bengali",
    "Gujarati",
    "Kannada",
    "Malayalam",
    "Punjabi",
    "Urdu",
    "Spanish",
    "French",
    "German"
]

# NLLB-200 Language Codes map
NLLB_LANGUAGE_CODES = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "Marathi": "mar_Deva",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Bengali": "ben_Beng",
    "Gujarati": "guj_Gujr",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Punjabi": "pan_Guru",
    "Urdu": "urd_Arab",
    "Spanish": "spa_Latn",
    "French": "fra_Latn",
    "German": "deu_Latn"
}

# gTTS Language Codes map
GTTS_LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

# langdetect code → human-readable language name
LANGDETECT_TO_LANGUAGE = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German"
}


def get_nllb_code(language_name):
    """Returns the NLLB-200 language code for a given human-readable language name."""
    return NLLB_LANGUAGE_CODES.get(language_name, "eng_Latn")


def get_gtts_code(language_name):
    """Returns the gTTS language code for a given human-readable language name."""
    return GTTS_LANGUAGE_CODES.get(language_name, "en")
