<div align="center">

# 🤖 LIMMA

**Language Interface Model for Machine Automation**

*Control your ESP8266/ESP32 devices with natural language commands*

---

[![PyPI Version](https://img.shields.io/pypi/v/limma?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/limma/)
[![Python Version](https://img.shields.io/pypi/pyversions/limma?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/limma/)
[![Downloads](https://img.shields.io/pypi/dm/limma?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/limma/)
[![License](https://img.shields.io/github/license/firoziya/limma?style=for-the-badge)](LICENSE)

[![GitHub Stars](https://img.shields.io/github/stars/firoziya/limma?style=for-the-badge&logo=github)](https://github.com/firoziya/limma)
[![GitHub Issues](https://img.shields.io/github/issues/firoziya/limma?style=for-the-badge&logo=github)](https://github.com/firoziya/limma/issues)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen?style=for-the-badge&logo=gitbook&logoColor=white)](https://pylimma.vercel.app/docs/)

</div>

---

## 🚀 What is LIMMA?

LIMMA is a **revolutionary Python SDK** that bridges the gap between natural language and IoT device control. Simply speak or type commands like *"turn on the living room lights"* or *"off the fan"*, and watch your ESP8266/ESP32 devices respond instantly!

### 🎯 Perfect For
- 🏠 **Smart Home Automation**
- 🚗 **Car Automation Systems** 
- 🏭 **Industrial IoT Control**
- 🤖 **Voice-Controlled Robotics**
- 📱 **Custom IoT Applications**

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🧠 **AI-Powered Processing**
- Natural language understanding
- Context-aware command parsing
- Multi-device coordination
- Smart error handling

### 🌐 **Network Intelligence**
- Auto-discovery of ESP devices
- WiFi configuration management
- Connection monitoring
- Network scanning utilities

</td>
<td width="50%">

### ⚡ **Real-time Control**
- Instant command execution
- Wait/delay support
- Batch operations
- Status monitoring

### 🔧 **Developer Friendly**
- Simple 3-line setup
- Comprehensive documentation
- Flexible device mapping
- Extensive examples

</td>
</tr>
</table>

---

## 📦 Installation

### Quick Install
```bash
pip install limma
```

### With Voice Support
```bash
pip install limma pyvoicekit
```

### Development Installation
```bash
git clone https://github.com/firoziya/limma.git
cd limma
pip install -e ".[dev]"
```

---

## 🎯 Quick Start

### 1️⃣ **Basic Setup**

```python
from limma import Limma, LimmaConfig

# Configure your setup
config = LimmaConfig(
    esp_ip="192.168.1.100",        # Your ESP device IP
    application_type="home",        # or "car", "office", etc.
    device_map={
        "living room light": "ch01",
        "bedroom fan": "ch02", 
        "kitchen light": "ch03",
        "garage door": "ch04"
    },
    api_key="your-limma-api-key",   # Get from https://pylimma.vercel.app
    reply=True                      # Enable voice responses
)

# Initialize LIMMA
limma = Limma(config)
```

### 2️⃣ **Execute Commands**

```python
# Single commands
success, reply = limma.execute_command("turn on the living room light")
if success:
    print(f"✅ {reply or 'Command executed successfully!'}")

# Complex commands
limma.execute_command("turn on all lights and wait 5 seconds then turn off the fan")

# Multiple device control
limma.execute_command("turn on the AC, set bedroom light to dim, and close the curtains")
```

### 3️⃣ **Voice Control Example**

```python
from limma import Limma, LimmaConfig
from pyvoicekit import listen, speak

def voice_control():
    # ... config setup ...
    limma = Limma(config)
    
    print("🎤 Voice control ready! Say something...")
    
    while True:
        command = listen()  # Listen for voice input
        if command:
            print(f"👤 You said: {command}")
            
            success, reply = limma.execute_command(command)
            
            if success and reply:
                speak(reply)  # Voice response
                print(f"🤖 LIMMA: {reply}")

voice_control()
```

---

## 🛠️ ESP8266/ESP32 Code

Upload this code to your ESP device:

<details>
<summary><b>📟 Click to view ESP8266 Arduino Code</b></summary>

```arduino
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "your-wifi-ssid";
const char* password = "your-wifi-password";

ESP8266WebServer server(80);

// Pin definitions
const int CH01_PIN = D1;  // Living room light
const int CH02_PIN = D2;  // Bedroom fan
const int CH03_PIN = D3;  // Kitchen light
const int CH04_PIN = D4;  // Garage door

void setup() {
  Serial.begin(115200);
  
  // Initialize pins
  pinMode(CH01_PIN, OUTPUT);
  pinMode(CH02_PIN, OUTPUT);
  pinMode(CH03_PIN, OUTPUT);
  pinMode(CH04_PIN, OUTPUT);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("✅ Connected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  
  // Setup routes
  server.on("/ch01on", []() { digitalWrite(CH01_PIN, HIGH); server.send(200, "text/plain", "CH01 ON"); });
  server.on("/ch01off", []() { digitalWrite(CH01_PIN, LOW); server.send(200, "text/plain", "CH01 OFF"); });
  server.on("/ch02on", []() { digitalWrite(CH02_PIN, HIGH); server.send(200, "text/plain", "CH02 ON"); });
  server.on("/ch02off", []() { digitalWrite(CH02_PIN, LOW); server.send(200, "text/plain", "CH02 OFF"); });
  // ... add more routes for other channels
  
  server.on("/ping", []() { server.send(200, "application/json", "{\"status\":\"pong\",\"device\":\"LIMMA-ESP8266\"}"); });
  
  server.begin();
}

void loop() {
  server.handleClient();
}

```
</details>

---

## 📚 Advanced Usage

### 🔍 **Auto-Discovery**


# Automatically find ESP devices on your network
```python
esp_ip = limma.auto_discover_esp()
if esp_ip:
    print(f"Found ESP device at: {esp_ip}")
    config.esp_ip = esp_ip
```

### ⚙️ **Device Management**


```python
# Check ESP connection
if limma.esp_manager.check_connection():
    print("✅ ESP is online")

# Get device status
status = limma.esp_manager.get_esp_status()
print(f"Device info: {status}")

# Configure WiFi remotely
limma.esp_manager.configure_wifi("new-ssid", "new-password")
```

### 🧠 **Context Management**

```python
# View command history
context_info = limma.get_context_info()
print(f"Remembered commands: {context_info['context_count']}")

# Clear context
limma.clear_context()
```

### 🔧 **Custom Applications**

```python
# Car automation
car_config = LimmaConfig(
    esp_ip="192.168.4.1",
    application_type="car",
    device_map={
        "headlights": "ch01",
        "engine": "ch02",
        "air conditioning": "ch03",
        "radio": "ch04"
    },
    api_key="your-api-key"
)

car_limma = Limma(car_config)
car_limma.execute_command("start the engine and turn on headlights")
```

---

## 🎛️ API Reference

### **LimmaConfig**
```python
LimmaConfig(
    esp_ip: str,                    # ESP device IP address
    application_type: str,          # "home", "car", "office", etc.
    device_map: dict,              # Device name -> channel mapping
    api_key: str,                  # LIMMA API key
    server_url: str = "...",       # LIMMA server URL
    reply: bool = False            # Enable voice replies
)
```

### **Limma Methods**
- `execute_command(command: str)` → `Tuple[bool, Optional[str]]`
- `send_to_server(command: str)` → `List[str]`
- `send_to_esp(functions: List[str])` → `Tuple[bool, Optional[str]]`
- `setup_esp(ssid, password)` → `bool`
- `auto_discover_esp()` → `Optional[str]`
- `get_context_info()` → `Dict`
- `clear_context()` → `None`

### **ESPManager Methods**
- `check_connection()` → `bool`
- `get_esp_status()` → `Dict`
- `reset_esp()` → `bool`
- `configure_wifi(ssid, password)` → `bool`

### **NetworkUtils Methods**
- `scan_network_for_esp(base_ip)` → `List[str]`
- `get_local_ip()` → `str`

---

## 💡 Examples & Use Cases

<details>
<summary><b>🏠 Smart Home Scenarios</b></summary>

```python
# Morning routine
limma.execute_command("good morning")
# Automatically: turn on lights, start coffee maker, open curtains

# Movie time
limma.execute_command("movie mode")
# Automatically: dim lights, turn on TV, close curtains

# Security mode
limma.execute_command("activate security")
# Automatically: turn off all lights, lock doors, arm sensors
```

</details>

<details>
<summary><b>🚗 Car Automation</b></summary>

```python
# Starting the car
limma.execute_command("start my car")
# Automatically: engine on, headlights on, AC on

# Parking mode
limma.execute_command("parking mode")
# Automatically: engine off, lights off, lock doors
```

</details>

<details>
<summary><b>🏭 Industrial Control</b></summary>

```python
# Production line control
limma.execute_command("start production line 1")
# Automatically: conveyor on, machines on, monitoring systems active

# Emergency stop
limma.execute_command("emergency stop all systems")
# Automatically: all equipment off, alarms on, safety protocols active

```
</details>

---

## 🐛 Troubleshooting

### **Common Issues**

| Issue | Solution |
|-------|----------|
| 🔴 ESP not found | Check IP address, WiFi connection |
| 🔴 API key error | Verify key at https://pylimma.vercel.app |
| 🔴 Command not working | Check device mapping, try simpler commands |
| 🔴 Network issues | Use `auto_discover_esp()` function |

### **Debug Mode**
```python

import logging
logging.basicConfig(level=logging.DEBUG)

# Now LIMMA will show detailed logs
limma.execute_command("turn on light")
```


## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Yash Kumar Firoziya**
- 📧 Email: [ykfiroziya@gmail.com](mailto:ykfiroziya@gmail.com)
- 🐱 GitHub: [@firoziya](https://github.com/firoziya)
- 🌐 Website: [pylimma.vercel.app](https://pylimma.vercel.app)

---

## 🙏 Acknowledgments

- Thanks to all contributors and users
- Inspired by the growing IoT community
- Built with ❤️ for makers and developers

---

## ⭐ Show Your Support

If you found LIMMA helpful, please consider:
- ⭐ **Starring** this repository
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 📢 **Sharing** with friends and colleagues

---

<div align="center">

**Made with ❤️ by [Yash Kumar Firoziya](https://github.com/firoziya)**

*Bringing the future of IoT control to everyone*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/firoziya/limma)
[![Documentation](https://img.shields.io/badge/Docs-4285F4?style=for-the-badge&logo=gitbook&logoColor=white)](https://pylimma.vercel.app/docs/)
[![PyPI](https://img.shields.io/badge/PyPI-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/limma/)

</div>
