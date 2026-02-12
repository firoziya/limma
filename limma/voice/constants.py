# Default configuration values
DEFAULT_VOICE_RATE = 150
DEFAULT_VOICE_VOLUME = 0.9
DEFAULT_TIMEOUT = 5
DEFAULT_PHRASE_TIME_LIMIT = 5
DEFAULT_ENGINE = 'pyttsx3'

DEFAULT_VOICE_GENDER = 'female'
SUPPORTED_GENDERS = ['male', 'female', 'neutral']

# Error messages
ERROR_MESSAGE = """
An error occurred in pyvoicelib. Please check:
- Microphone is connected and working
- Internet connection (for speech recognition)
- Required dependencies are installed

For more information and troubleshooting, visit:
https://github.com/Yazirofi/pyvoicelib
"""