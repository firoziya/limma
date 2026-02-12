import os

CONFIG = {
    "provider": None,
    "api_key": None,
    "model": None,
    "base_url": None,
}

def config(provider=None, api_key=None, model=None, base_url=None):
    CONFIG["provider"] = provider or os.getenv("LLM_PROVIDER")
    CONFIG["api_key"] = api_key or os.getenv("LLM_API_KEY")
    CONFIG["model"] = model or os.getenv("LLM_MODEL")
    CONFIG["base_url"] = base_url or os.getenv("LLM_BASE_URL")


