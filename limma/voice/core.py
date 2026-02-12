import warnings

import speech_recognition as sr
from typing import Optional
from .constants import *
from .exceptions import *
from .utils import initialize_components

# Global components initialized on first use
_recognizer = None
_engine = None


def _get_components():
    """Lazy initialization of global components"""
    global _recognizer, _engine
    if _recognizer is None or _engine is None:
        _recognizer, _engine = initialize_components()
    return _recognizer, _engine


def speak(text: str, wait: bool = True, rate: int = None, volume: float = None):
    """
    Convert text to speech and speak it out loud (standalone function).

    Args:
        text: Text to speak
        wait: Whether to wait for speech to complete
        rate: Optional speech rate (words per minute)
        volume: Optional volume level (0.0 to 1.0)
    """
    try:
        recognizer, engine = _get_components()

        if rate is not None:
            engine.setProperty('rate', rate)
        if volume is not None:
            if 0 <= volume <= 1:
                engine.setProperty('volume', volume)
            else:
                raise ValueError("Volume must be between 0.0 and 1.0")

        engine.say(text)
        if wait:
            engine.runAndWait()
    except Exception as e:
        raise SpeechError(f"Text-to-speech error: {str(e)}")

def listen(
        timeout: int = DEFAULT_TIMEOUT,
        phrase_time_limit: int = DEFAULT_PHRASE_TIME_LIMIT
) -> Optional[str]:
    """
    Listen for user speech and return recognized text (standalone function).

    Args:
        timeout: Timeout in seconds for listening
        phrase_time_limit: Maximum time for a phrase

    Returns:
        Recognized text or None if no speech detected
    """
    try:
        recognizer, engine = _get_components()

        with sr.Microphone() as source:
            print("Listening...")  # Can be made configurable later
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
            return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        raise ListenTimeoutError("No speech detected within timeout period")
    except sr.UnknownValueError:
        return None
    except Exception as e:
        raise AudioCaptureError(f"Error capturing audio: {str(e)}")


class VoiceAssistant:
    def __init__(self,
                 voice_rate: int = DEFAULT_VOICE_RATE,
                 voice_volume: float = DEFAULT_VOICE_VOLUME,
                 voice_gender: str = DEFAULT_VOICE_GENDER):
        """
        Initialize the voice assistant.

        Args:
            voice_rate: Words per minute
            voice_volume: Volume level (0.0 to 1.0)
            voice_gender: Voice gender ('male', 'female', or 'neutral')
        """
        try:
            self.recognizer, self.engine = initialize_components()
            self.set_voice_rate(voice_rate)
            self.set_voice_volume(voice_volume)
            self.set_voice_gender(voice_gender)
        except Exception as e:
            raise InitializationError(str(e))

    def set_voice_gender(self, gender: str):
        """
        Set the voice gender.

        Args:
            gender: 'male', 'female', or 'neutral'

        Raises:
            ValueError: If gender is not supported
            SpeechError: If no voices are available
        """
        if gender not in SUPPORTED_GENDERS:
            raise ValueError(f"Unsupported gender. Choose from: {SUPPORTED_GENDERS}")

        voices = self.engine.getProperty("voices")
        if not voices:
            raise SpeechError("No voices available on this system")

        gender = gender.lower()

        # Try exact match in voice name
        for voice in voices:
            if gender in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                return

        # Fallback: try any supported gender keyword
        for voice in voices:
            if any(g in voice.name.lower() for g in SUPPORTED_GENDERS):
                self.engine.setProperty("voice", voice.id)
                warnings.warn(f"Exact '{gender}' voice not found. Using closest match: {voice.name}")
                return

        # Last fallback: default to first voice
        self.engine.setProperty("voice", voices[0].id)
        warnings.warn(f"No '{gender}' voice found. Using default system voice.")

    def get_available_voices(self):
        """Return list of available voice names"""
        return [v.name for v in self.engine.getProperty("voices")]

    def set_voice_rate(self, rate: int):
        self.engine.setProperty("rate", rate)

    def set_voice_volume(self, volume: float):
        if 0 <= volume <= 1:
            self.engine.setProperty("volume", volume)
        else:
            raise ValueError("Volume must be between 0.0 and 1.0")

    def speak(self, text: str, wait: bool = True):
        """Convert text to speech and speak it out loud."""
        try:
            self.engine.say(text)
            if wait:
                self.engine.runAndWait()
        except Exception as e:
            raise SpeechError(f"Text-to-speech error: {str(e)}")

    def listen(self,
               timeout: int = DEFAULT_TIMEOUT,
               phrase_time_limit: int = DEFAULT_PHRASE_TIME_LIMIT) -> Optional[str]:
        """Listen for user speech and return the recognized text."""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                return self.recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            raise ListenTimeoutError("No speech detected within timeout period")
        except sr.UnknownValueError:
            return None
        except Exception as e:
            raise AudioCaptureError(f"Error capturing audio: {str(e)}")

    def simple_conversation(self, prompt: str):
        """A simple conversation helper that speaks and then listens."""
        self.speak(prompt)
        return self.listen()