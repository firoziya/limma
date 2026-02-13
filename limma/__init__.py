"""
LIMMA - Language Interface Model for Machine Automation
A Python package for controlling ESP8266/ESP32 devices using natural language.
"""

__version__ = "0.2.1"
__author__ = "Yash Kumar Firoziya"
__email__ = "ykfiroziya@gmail.com"

from .core import Limma, LimmaConfig, ContextManager, ESPManager, NetworkUtils
from .llm.__init__ import config, generate, chat, reset_chat
from .voice.__init__ import speak, listen

__all__ = [
    "Limma",
    "LimmaConfig", 
    "ContextManager",
    "ESPManager",
    "NetworkUtils",
    "config",
    "generate",
    "chat",
    "reset_chat",
    "speak",
    "listen",
]