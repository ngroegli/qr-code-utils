"""Configuration management for QR Code Utils."""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Manages application configuration."""

    DEFAULT_CONFIG_DIR = Path.home() / ".qr-utils"
    DEFAULT_CONFIG_FILE = "config.json"
    DEFAULT_LOGS_DIR = "logs"
    DEFAULT_OUTPUT_DIR = "output"

    DEFAULT_QR_SETTINGS = {
        "version": 1,
        "error_correction": "H",  # L, M, Q, H
        "box_size": 10,
        "border": 4,
        "fill_color": "black",
        "back_color": "white"
    }

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_dir: Custom configuration directory path
        """
        self.config_dir = config_dir or self.DEFAULT_CONFIG_DIR
        self.config_file = self.config_dir / self.DEFAULT_CONFIG_FILE
        self.logs_dir = self.config_dir / self.DEFAULT_LOGS_DIR
        self.output_dir = self.config_dir / self.DEFAULT_OUTPUT_DIR

        self._config: Dict[str, Any] = {}
        self._ensure_directories()
        self._load_config()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self):
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.config_file}. Using defaults.")
                self._config = self._get_default_config()
        else:
            self._config = self._get_default_config()
            self._save_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "qr_settings": self.DEFAULT_QR_SETTINGS.copy(),
            "output_format": "png",
            "default_output_dir": str(self.output_dir),
            "vcard_defaults": {
                "version": "3.0"
            }
        }

    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., 'qr_settings.version')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any, save: bool = True):
        """Set configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
            save: Whether to save to file immediately
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

        if save:
            self._save_config()

    def get_qr_settings(self) -> Dict[str, Any]:
        """Get QR code settings."""
        return self.get('qr_settings', self.DEFAULT_QR_SETTINGS.copy())

    def get_output_path(self, filename: str) -> Path:
        """Get full output path for a file.

        Args:
            filename: Output filename

        Returns:
            Full path to output file
        """
        return self.output_dir / filename
