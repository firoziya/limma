"""
LIMMA - Language Interface Model for Machine Automation
A Python package for controlling ESP8266/ESP32 devices using natural language.
"""

__version__ = "0.1.0"
__author__ = "Yash Kumar Firoziya"
__email__ = "ykfiroziya@gmail.com"

from .core import Limma, LimmaConfig, ContextManager, ESPManager, NetworkUtils

__all__ = [
    "Limma",
    "LimmaConfig", 
    "ContextManager",
    "ESPManager",
    "NetworkUtils"
]