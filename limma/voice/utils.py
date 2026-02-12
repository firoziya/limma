import sys
from .constants import ERROR_MESSAGE
from .exceptions import VoiceLibError, InitializationError, SpeechError, AudioCaptureError, ListenTimeoutError


def check_python_version():
    """Check if the Python version is supported"""
    if sys.version_info < (3, 6):
        raise VoiceLibError("pyvoicelib requires Python 3.6 or higher")


def initialize_components():
    """Initialize speech components with error handling"""
    check_python_version()

    try:
        import speech_recognition as sr
        import pyttsx3
        import pyaudio
    except ImportError as e:
        raise InitializationError(
            f"Required package not found: {str(e)}\n{ERROR_MESSAGE}"
        )

    try:
        recognizer = sr.Recognizer()
        engine = pyttsx3.init()
        return recognizer, engine
    except Exception as e:
        raise InitializationError(
            f"Failed to initialize components: {str(e)}\n{ERROR_MESSAGE}"
        )