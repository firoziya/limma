from .config import CONFIG
from .prompts import format_prompt
from .providers import get_provider

def generate(prompt):
    provider = get_provider(CONFIG["provider"])
    formatted = format_prompt(prompt)
    return provider.send(formatted)
