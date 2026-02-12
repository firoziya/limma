# LIMMA

**Language Interface Model for Machine Automation**

<div align="center">

[![Downloads](https://static.pepy.tech/badge/limma)](https://pepy.tech/projects/limma)
[![PyPI Version](https://img.shields.io/pypi/v/limma.svg)](https://pypi.org/project/limma/)
![Python Version](https://img.shields.io/pypi/pyversions/limma.svg)
[![License](https://img.shields.io/github/license/firoziya/limma)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/firoziya/limma?style=social)](https://github.com/firoziya/limma)

</div>

LIMMA is a Python SDK that lets you control **ESP8266/ESP32** devices using **natural language commands**.  
It connects with the [LIMMA API](https://pylimma.vercel.app/) to translate user instructions into device function calls, then executes them over your local network.  

---

> Author: Yash Kumar Firoziya

---

## ✨ Features

### Core Features
- 🔌 **ESP Device Management** – connect, reset, WiFi setup, status check  
- 🌐 **Natural Language → Device Control** – powered by the LIMMA server  
- 🧠 **Context Manager** – remembers previous commands for context-aware parsing  
- 📡 **Network Utilities** – auto-discover ESP devices in your LAN  
- ⚙️ **Flexible Execution** – supports `wait()`, device mapping, and `reply` messages  

### 🆕 New in v0.2.0+ – Multi-Provider LLM Integration
- 🤖 **Unified LLM Interface** – Single API for multiple LLM providers via `limma.llm`
- 🔄 **Provider Agnostic** – Switch between OpenAI, Gemini, Mistral, Groq with one line
- 🧠 **Consistent Message Format** – Same request style across all providers
- 🔐 **Flexible Configuration** – Use env vars, inline setup, or config files
- 🚀 **No Vendor Lock-In** – Swap providers without rewriting logic
- 📜 **Role-Based Conversations** – System, user, assistant message support
- 🛡️ **Automatic Token Handling** – Prevents context overflows

### 🆕 New in v0.2.0+ – Voice Capabilities
- 🎙️ **Cross-Platform Voice** – Speech recognition & text-to-speech via `limma.voice`
- 🔊 **Voice Customization** – Adjust rate, volume, and gender (male/female/neutral)
- 🗣️ **Simple API** – Both standalone functions and VoiceAssistant class
- 🎯 **Beginner-Friendly** – Add voice control to your projects in minutes
- 🎚️ **Voice Settings** – List available voices, change gender on the fly

---

## 📦 Installation

```bash
pip install limma
```

### Install with Optional Dependencies

```bash
# For LLM features
pip install limma[llm]

# For voice features
pip install limma[voice]

# For all features
pip install limma[all]
```

---

## 🚀 Quick Start

### Basic ESP Control

```python
from limma import Limma, LimmaConfig

config = LimmaConfig(
    esp_ip="192.168.1.100",
    application_type="home",
    device_map={"fan": "ch02", "light": "ch01"},
    api_key="your-api-key"
)

limma = Limma(config)
limma.execute_command("turn on the fan")
```

---

## 🆕 New in v0.2.0: LLM Integration

### Unified Interface for Multiple LLM Providers

```python
from limma.llm import config, generate, chat

# Configure once, use anywhere
config(
    provider="openai",  # or "gemini", "mistral", "groq"
    api_key="your-api-key",
    model="gpt-4"
)

# Generate text
response = generate("Explain IoT in simple terms")
print(response)

# Interactive chat
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print(f"AI: {chat(user_input)}")
```

### Switch Providers Instantly

```python
from limma.llm import config, generate

# Start with OpenAI
config(provider="openai", api_key="sk-...", model="gpt-4")
print(generate("Hello!"))

# Switch to Gemini (free tier available)
config(provider="gemini", api_key="AIza...", model="gemini-2.5-flash")
print(generate("Hello again!"))

# Switch to Groq for ultra-fast inference
config(provider="groq", api_key="gsk_...", model="mixtral-8x7b-32768")
print(generate("Fast response!"))
```

### Using Environment Variables

```bash
# .env file
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key
LLM_MODEL=gpt-4
```

```python
from limma.llm import config, generate

config()  # Auto-loads from environment
print(generate("What's new in Python 3.12?"))
```

### Supported LLM Providers

| Provider | Models | Use Case |
|----------|--------|----------|
| **OpenAI** | GPT-4, GPT-3.5-turbo | General purpose, best quality |
| **Google Gemini** | Gemini 2.5/1.5 Flash | Free tier available, fast |
| **Mistral** | Mistral Large/Small | Open source, efficient |
| **Groq** | Mixtral, Llama 2 | Ultra-fast inference |

---

## 🆕 New in v0.2.0: Voice Integration

### Simple Voice Control

```python
from limma.voice import speak, listen

# Text-to-speech
speak("Hello! I'm your voice-enabled LIMMA assistant")

# Speech recognition
try:
    command = listen()
    print(f"You said: {command}")
    speak(f"Executing: {command}")
except Exception as e:
    speak("Sorry, I didn't catch that")
```

### VoiceAssistant Class

```python
from limma.voice import VoiceAssistant

# Create a customized voice assistant
assistant = VoiceAssistant(
    voice_rate=160,      # Words per minute
    voice_volume=0.8,    # Volume (0.0 - 1.0)
    voice_gender="female"  # male, female, or neutral
)

# Speak with the configured voice
assistant.speak("How can I help you with your ESP devices?")

# Listen for commands
command = assistant.listen()
if command:
    print(f"Command received: {command}")
    
# Change voice settings on the fly
assistant.set_voice_gender("male")
assistant.set_voice_rate(180)
assistant.speak("Voice settings updated")
```

### Voice + ESP Control Combined

```python
from limma import Limma, LimmaConfig
from limma.voice import VoiceAssistant

# Initialize voice and ESP control
voice = VoiceAssistant(voice_gender="female")
limma = Limma(LimmaConfig(esp_ip="auto", api_key="your-key"))

# Voice-controlled home automation
voice.speak("Voice control ready. Say a command.")

while True:
    command = voice.listen(timeout=5)
    if command:
        if "exit" in command.lower():
            voice.speak("Goodbye!")
            break
        success = limma.execute_command(command)
        if success:
            voice.speak("Command executed successfully")
        else:
            voice.speak("Failed to execute command")
```

### Voice Customization Examples

```python
from limma.voice import VoiceAssistant

va = VoiceAssistant()

# List available system voices
available_voices = va.get_available_voices()
print(f"Available voices: {available_voices}")

# Test different voice genders
va.set_voice_gender("female")
va.speak("This is the female voice")

va.set_voice_gender("male") 
va.speak("This is the male voice")

# Adjust speech rate and volume
va.set_voice_rate(200)  # Faster speech
va.set_voice_volume(0.5)  # Quieter
va.speak("This is fast and quiet")

va.set_voice_rate(120)  # Slower speech
va.set_voice_volume(1.0)  # Louder
va.speak("This is slow and loud")
```

---

## 🎯 Complete Example: Voice + LLM + ESP Control

```python
from limma import Limma, LimmaConfig
from limma.voice import VoiceAssistant
from limma.llm import config as llm_config, generate

# Configure LLM for command understanding
llm_config(
    provider="gemini",  # Free tier
    api_key="your-gemini-key",
    model="gemini-2.5-flash"
)

# Initialize voice assistant
voice = VoiceAssistant(voice_gender="female")

# Setup ESP control
limma = Limma(LimmaConfig(
    esp_ip="auto",
    application_type="home",
    device_map={"fan": "ch02", "light": "ch01", "ac": "ch03"},
    api_key="limma-api-key"
))

# Intelligent voice-controlled automation
voice.speak("Smart home system activated")

while True:
    command = voice.listen()
    
    if command:
        if "exit" in command.lower():
            voice.speak("Shutting down")
            break
            
        # Use LLM to understand complex commands
        enhanced_command = generate(
            f"Convert this home automation request into a simple command: '{command}'. "
            f"Available devices: fan, light, ac. Response should be brief."
        )
        
        print(f"Original: {command}")
        print(f"Interpreted: {enhanced_command}")
        
        # Execute on ESP
        if limma.execute_command(enhanced_command):
            voice.speak("Done")
        else:
            voice.speak("I couldn't do that")
```

---

## 📚 API Reference

### Core Modules
- `Limma` – Main SDK controller
- `LimmaConfig` – Configuration container
- `ESPManager` – ESP device operations
- `ContextManager` – Command history and context
- `NetworkUtils` – Network discovery utilities

### 🆕 LLM Module (`limma.llm`)
- `config(**kwargs)` – Set provider, API key, model
- `generate(prompt, **kwargs)` – Single text generation
- `generate_stream(prompt, **kwargs)` – Streaming response
- `chat(message)` – Conversational interface
- `reset_chat()` – Clear conversation history

### 🆕 Voice Module (`limma.voice`)
- `speak(text, **kwargs)` – Text-to-speech conversion
- `listen(timeout)` – Speech recognition
- `VoiceAssistant` – Class-based voice interface
  - `set_voice_rate(rate)` – Adjust speech speed
  - `set_voice_volume(volume)` – Adjust volume
  - `set_voice_gender(gender)` – Change voice gender
  - `get_available_voices()` – List system voices
  - `simple_conversation(prompt)` – Quick Q&A

---

## 🛡️ Error Handling

```python
from limma.voice.exceptions import ListenTimeoutError, AudioCaptureError
from limma.llm.exceptions import AuthenticationError, ModelNotFoundError

try:
    response = generate("Hello")
except AuthenticationError:
    print("Check your API key")
except ModelNotFoundError:
    print("Invalid model name")
```

---

## 📦 Dependencies

- **Core**: `requests`
- **LLM Module**: `requests` (no additional deps)
- **Voice Module**: `SpeechRecognition`, `pyttsx3`, `pyaudio`

---

## 📄 License

Licensed under the **Apache License 2.0**.
See [LICENSE](./LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⭐ Support

If you find LIMMA useful, please give it a star on GitHub!

---

**Now LIMMA is not just an ESP control SDK – it's a complete toolkit for building intelligent, voice-controlled, multi-provider AI automation systems.** 🚀