import requests
from ..config import CONFIG
from .base import ProviderBase

class MistralProvider(ProviderBase):
    def send(self, messages):
        url = CONFIG["base_url"] or "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": CONFIG["model"],
            "messages": messages
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"]
