import pyttsx3

def speak(
    text: str,
    female: bool = False,
    rate: int = 150,
    volume: float = 0.9
) -> None:

    # ---------- validation ----------
    if text is None:
        raise TypeError("text cannot be None")

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if not text.strip():
        raise ValueError("text cannot be empty")

    if not (0.0 <= volume <= 1.0):
        raise ValueError("volume must be between 0.0 and 1.0")

    if not isinstance(rate, int) or rate <= 0:
        raise ValueError("rate must be a positive integer")

    try:
        engine = pyttsx3.init()   # ✅ create fresh engine

        voices = engine.getProperty("voices")

        if female:
            female_keywords = [
                "female", "woman", "zira",
                "samantha", "victoria", "anna"
            ]

            for voice in voices:
                if any(k in voice.name.lower() for k in female_keywords):
                    engine.setProperty("voice", voice.id)
                    break

        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        raise RuntimeError(f"TTS engine failure: {e}")