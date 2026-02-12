import requests
from typing import List, Dict, Any
from ..config import CONFIG
from .base import ProviderBase


def validate_config():
    """Validate required configuration values"""
    if not CONFIG.get("api_key"):
        raise ValueError("GROQ_API_KEY is not set in configuration")
    if not CONFIG.get("model"):
        raise ValueError("Model is not specified in configuration")

    # Set default URL if not provided
    if "base_url" not in CONFIG or not CONFIG["base_url"]:
        CONFIG["base_url"] = "https://api.groq.com/openai/v1/chat/completions"


class GroqProvider(ProviderBase):
    def __init__(self):
        validate_config()

    def send(self, messages: List[Dict[str, str]]) -> str:
        """Send messages to Groq API and return the response.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
                      Example: [{"role": "user", "content": "Hello"}]

        Returns:
            The content of the response message

        Raises:
            Exception: If API request fails or response is invalid
        """
        try:
            # Validate messages format
            if not messages or not isinstance(messages, list):
                raise ValueError("Messages must be a non-empty list of message dictionaries")

            for msg in messages:
                if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                    raise ValueError("Each message must be a dictionary with 'role' and 'content' keys")

            response = requests.post(
                url=CONFIG["base_url"],
                headers={
                    "Authorization": f"Bearer {CONFIG['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": CONFIG["model"],
                    "messages": messages,
                    "temperature": CONFIG.get("temperature", 0.7)
                },
                timeout=30
            )

            res = response.json()

            # Check for errors first
            if "error" in res:
                error_msg = res["error"].get("message", "Unknown error")
                raise Exception(f"Groq API Error: {error_msg}")

            if not response.ok:
                raise Exception(f"API request failed with status {response.status_code}")

            # Safely extract response content
            try:
                return res["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                raise Exception(f"Unexpected response format: {str(e)}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")