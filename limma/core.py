import time
import json
import logging
import requests
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import socket
import urllib.request
import subprocess
import platform

# Set up logging
logger = logging.getLogger(__name__)

class ContextManager:
    """Manages context history for command processing."""
    
    def __init__(self, max_contexts: int = 7):
        """
        Initialize the ContextManager.
        
        Args:
            max_contexts (int): Maximum number of contexts to store
        """
        self.max_contexts = max_contexts
        self.context_queue = []
    
    def add_context(self, command: str, response: List[str]) -> None:
        """Add context to the queue, maintaining max size"""
        context_item = {
            "command": command, 
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        self.context_queue.append(context_item)
        if len(self.context_queue) > self.max_contexts:
            self.context_queue.pop(0)
    
    def get_context_string(self) -> str:
        """Convert context queue to formatted string for prompt"""
        if not self.context_queue:
            return ""
        
        context_str = "Previous commands and their function calls:\n"
        for i, item in enumerate(self.context_queue, 1):
            # Convert response list to readable string
            response_str = ", ".join([f'"{func}"' for func in item['response']])
            context_str += f"{i}. Command: '{item['command']}' -> Functions: [{response_str}]\n"
        return context_str
    
    def clear_context(self) -> None:
        """Clear the context queue"""
        self.context_queue = []


class LimmaConfig:
    """Configuration class for LIMMA."""
    
    def __init__(self, esp_ip: str, application_type: str, device_map: dict, 
                api_key: str, server_url: str = "https://limma-api.onrender.com/parse", 
                reply: bool = False):
        """
        Initialize LIMMA configuration.
        
        Args:
            esp_ip (str): IP address of the ESP device
            application_type (str): Type of application (e.g., "home or car")
            device_map (dict): Mapping of device names to functions
            api_key (str): API key for LIMMA server
            server_url (str): URL of the LIMMA server
            reply (bool): Whether to enable reply functionality
            
        Raises:
            ValueError: If any required parameter is invalid
        """
        # Validate parameters
        if not isinstance(esp_ip, str) or not esp_ip:
            raise ValueError("ESP IP must be a non-empty string")
        
        if not isinstance(application_type, str) or not application_type:
            raise ValueError("Application type must be a non-empty string")
        
        if not isinstance(device_map, dict):
            raise ValueError("Device map must be a dictionary")
        
        if not isinstance(api_key, str) or not api_key:
            raise ValueError("API key must be a non-empty string")
        
        if not isinstance(server_url, str) or not server_url:
            raise ValueError("Server URL must be a non-empty string")
        
        self.esp_ip = esp_ip
        self.application_type = application_type
        self.device_map = device_map
        self.server_url = server_url
        self.api_key = api_key
        self.reply = reply


class ESPManager:
    """Manages communication with ESP devices."""
    
    def __init__(self, esp_ip: str):
        """
        Initialize ESPManager.
        
        Args:
            esp_ip (str): IP address of the ESP device
        """
        self.esp_ip = esp_ip
    
    def check_connection(self) -> bool:
        """Check if ESP is reachable"""
        try:
            response = requests.get(f"http://{self.esp_ip}/ping", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"ESP connection check failed: {e}")
            return False
    
    def get_esp_status(self) -> Dict:
        """Get ESP status information"""
        try:
            response = requests.get(f"http://{self.esp_ip}/status", timeout=5)
            if response.status_code == 200:
                return response.json()
            logger.warning(f"Failed to get ESP status: HTTP {response.status_code}")
            return {"error": "Failed to get status"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting ESP status: {e}")
            return {"error": str(e)}
    
    def reset_esp(self) -> bool:
        """Reset ESP device"""
        try:
            response = requests.get(f"http://{self.esp_ip}/reset", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"ESP reset failed: {e}")
            return False
    
    def configure_wifi(self, ssid: str, password: str) -> bool:
        """Configure WiFi on ESP"""
        try:
            payload = {"ssid": ssid, "password": password}
            response = requests.post(f"http://{self.esp_ip}/wifi-config", 
                                   json=payload, timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"WiFi configuration failed: {e}")
            return False


class NetworkUtils:
    """Network utility functions."""
    
    @staticmethod
    def scan_network_for_esp(base_ip: Optional[str] = None) -> List[str]:
        """Scan network for ESP devices"""
        if base_ip is None:
            local_ip = NetworkUtils.get_local_ip()
            base_ip = ".".join(local_ip.split(".")[:-1])
        
        esp_devices = []
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((ip, 80))
                if result == 0:
                    try:
                        response = requests.get(f"http://{ip}/ping", timeout=1)
                        if "ESP" in response.text or response.status_code == 200:
                            esp_devices.append(ip)
                    except:
                        pass
                sock.close()
            except:
                pass
        return esp_devices
    
    @staticmethod
    def get_local_ip() -> str:
        """Get local IP address"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception as e:
            logger.warning(f"Could not determine local IP: {e}")
            return "127.0.0.1"


class Limma:
    """Main LIMMA class for processing natural language commands for IoT devices."""
    
    def __init__(self, config: LimmaConfig):
        """
        Initialize LIMMA.
        
        Args:
            config (LimmaConfig): Configuration object for LIMMA
            
        Example:
            >>> config = LimmaConfig(esp_ip="192.168.1.100", 
            >>>                     application_type="home",
            >>>                     device_map={
                                        "fan": "ch02",
                                        "light": "ch01", 
                                        "ac": "ch03",
                                        "tv": "ch04",
                                        "bedroom light": "ch05",
                                        "kitchen light": "ch06"
                                    },
            >>> api_key="your_api_key")
            >>> limma = Limma(config)
            >>> success, reply = limma.execute_command("turn on the light")
        """
        self.config = config
        self.context_manager = ContextManager()
        self.esp_manager = ESPManager(config.esp_ip)
        self.session = requests.Session()  # Reuse connections
        
    def send_to_server(self, command: str) -> List[str]:
        """Send command to LIMMA server for processing"""
        context_history = self.context_manager.get_context_string()
        
        payload = {
            "command": command,
            "application_type": self.config.application_type,
            "device_map": self.config.device_map,
            "reply": self.config.reply,
            "api_key": self.config.api_key,
            "context_history": context_history 
        }
        
        try:
            logger.debug(f"Sending command to server: {command}")
            response = self.session.post(self.config.server_url, json=payload, timeout=10)
            
            if response.status_code == 401:
                logger.error("API key authentication failed")
                return []
            elif response.status_code != 200:
                logger.error(f"Server returned HTTP {response.status_code}")
                return []
            
            data = response.json()
            
            if isinstance(data, dict) and "functions" in data:
                functions = data["functions"]
                # Add to context for future reference
                self.context_manager.add_context(command, functions)
                logger.debug(f"Received functions from server: {functions}")
                return functions
            
            return data if isinstance(data, list) else []
            
        except requests.exceptions.Timeout:
            logger.error("Server request timed out")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error contacting server: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error processing server response: {e}")
            return []
    
    def send_to_esp(self, functions: List[str]) -> Tuple[bool, Optional[str]]:
        """Send function calls to ESP device"""
        success = True
        reply_text = None
        
        for fn in functions:
            try:
                if fn.startswith("wait(") and fn.endswith(")"):
                    # Handle wait command
                    seconds_str = fn[5:-1]  # Extract number from wait(N)
                    try:
                        seconds = int(seconds_str)
                        logger.debug(f"Waiting for {seconds} seconds")
                        time.sleep(seconds)
                    except ValueError:
                        logger.error(f"Invalid wait time: {seconds_str}")
                        success = False
                    continue
                
                elif fn.startswith("reply:"):
                    # Handle reply command
                    reply_text = fn.replace("reply:", "").strip()
                    logger.debug(f"Reply text: {reply_text}")
                    continue
                
                elif fn.endswith("()"):
                    # Handle ESP function call
                    fn_clean = fn.replace("()", "")
                    url = f"http://{self.config.esp_ip}/{fn_clean}"
                    
                    logger.debug(f"Calling ESP function: {url}")
                    response = self.session.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        logger.debug(f"ESP function {fn_clean} executed successfully")
                    else:
                        logger.error(f"ESP function {fn_clean} failed: HTTP {response.status_code}")
                        success = False
                
                else:
                    logger.warning(f"Unknown function format: {fn}")
                    success = False
                    
            except requests.exceptions.Timeout:
                logger.error(f"ESP function {fn} timed out")
                success = False
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error calling ESP function {fn}: {e}")
                success = False
            except Exception as e:
                logger.error(f"Unexpected error calling ESP function {fn}: {e}")
                success = False
        
        return success, reply_text
    
    def execute_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """Execute a complete command (server + ESP)"""
        logger.info(f"Executing command: {command}")
        
        # Get functions from server
        functions = self.send_to_server(command)
        if not functions:
            logger.error("No functions returned from server")
            return False, None
        
        # Send to ESP
        return self.send_to_esp(functions)

    
    def setup_esp(self, ssid: Optional[str] = None, password: Optional[str] = None) -> bool:
        """Automated ESP setup"""
        logger.info("Setting up ESP device")
        
        # Check connection
        if not self.esp_manager.check_connection():
            logger.error("ESP device is not reachable")
            return False
        
        # Configure WiFi if credentials provided
        if ssid and password:
            logger.info(f"Configuring WiFi: {ssid}")
            if self.esp_manager.configure_wifi(ssid, password):
                logger.info("WiFi configured successfully")
            else:
                logger.error("WiFi configuration failed")
                return False
        
        # Get ESP status
        status = self.esp_manager.get_esp_status()
        logger.info(f"ESP status: {status}")
        
        return True
    
    def auto_discover_esp(self) -> Optional[str]:
        """Automatically discover ESP devices on network"""
        logger.info("Scanning network for ESP devices")
        esp_devices = NetworkUtils.scan_network_for_esp()
        
        if esp_devices:
            logger.info(f"Found ESP devices: {esp_devices}")
            return esp_devices[0]  # Return first found device
        else:
            logger.warning("No ESP devices found on network")
            return None
    
    def get_context_info(self) -> Dict:
        """Get context information"""
        return {
            "context_count": len(self.context_manager.context_queue),
            "max_contexts": self.context_manager.max_contexts,
            "context_history": self.context_manager.context_queue
        }
    
    def clear_context(self) -> None:
        """Clear context history"""
        logger.info("Clearing context history")
        self.context_manager.clear_context()
    
    def close(self) -> None:
        """Clean up resources"""
        logger.info("Closing LIMMA session")
        self.session.close()