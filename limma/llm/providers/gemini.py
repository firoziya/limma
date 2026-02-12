import requests
from ..config import CONFIG
from .base import ProviderBase


class GeminiProvider(ProviderBase):
    def send(self, messages):
        url = (
            CONFIG.get("base_url")
            or f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{CONFIG['model']}:generateContent"
        )

        # Convert messages into Gemini contents format
        contents = []
        for m in messages:
            contents.append({
                "parts": [
                    {"text": m["content"]}
                ]
            })

        payload = {
            "contents": contents
        }

        headers = {
            "x-goog-api-key": CONFIG["api_key"],
            "Content-Type": "application/json"
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise RuntimeError(f"Unexpected Gemini response: {data}")
