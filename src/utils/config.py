"""
LAM-Action-Guard Configuration Module
Centralized configuration management for the project.
"""

import json
import os
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for LAM-Action-Guard."""
    
    DEFAULT_CONFIG = {
        "scanner": {
            "timeout": 10,
            "max_retries": 3,
            "user_agent": "LAM-Action-Guard/1.0",
            "follow_redirects": True
        },
        "output": {
            "format": "json",
            "verbose": False,
            "color": True
        },
        "security": {
            "verify_ssl": True,
            "rate_limit": 1.0  # requests per second
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    return self._merge_configs(self.DEFAULT_CONFIG, user_config)
            except json.JSONDecodeError:
                print(f"[⚠] Invalid config file, using defaults")
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def _merge_configs(self, default: Dict, override: Dict) -> Dict:
        """Deep merge two configuration dictionaries."""
        result = default.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get a configuration value by nested keys."""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def save(self) -> None:
        """Save current configuration to file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
        print(f"[✓] Configuration saved to {self.config_path}")


# Global config instance
_config: Optional[Config] = None

def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
