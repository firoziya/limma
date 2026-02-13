import speech_recognition as sr

def listen(timeout: int = 5):
    """
    Listen to microphone and convert speech to text.
    :param timeout: Duration to wait for speech input.
    :return: Recognized text or None
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            print("🔄 Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            print("❌ Timeout reached. No speech detected.")
        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
        except sr.RequestError as e:
            print(f"❌ API Error: {e}")
    return None