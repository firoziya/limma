from .openai import OpenAIProvider
from .gemini import GeminiProvider
from .mistral import MistralProvider
from .groq import GroqProvider
from .base import ProviderBase

def get_provider(name) -> ProviderBase:
    name = name.lower()
    if name == "openai":
        return OpenAIProvider()
    elif name == "gemini":
        return GeminiProvider()
    elif name == "groq":
        return GroqProvider()
    elif name == "mistral":
        return MistralProvider()
    else:
        raise ValueError(f"Unknown provider: {name}")