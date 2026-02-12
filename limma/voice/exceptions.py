ERROR_MESSAGE = "\nFor more information and troubleshooting, visit: https://github.com/Yazirofi/pyvoicelib"

class VoiceLibError(Exception):
    """Base exception for pyvoicelib errors"""
    def __init__(self, message=None):
        if message and ERROR_MESSAGE not in message:
            message = f"{message}{ERROR_MESSAGE}"
        super().__init__(message or ERROR_MESSAGE)

class ListenTimeoutError(VoiceLibError):
    """Raised when listening times out"""
    pass

class AudioCaptureError(VoiceLibError):
    """Raised when there's an error capturing audio"""
    pass

class SpeechError(VoiceLibError):
    """Raised when there's an error with text-to-speech"""
    pass

class InitializationError(VoiceLibError):
    """Raised when there's an error initializing components"""
    pass