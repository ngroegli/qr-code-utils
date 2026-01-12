"""
Unit tests for the Config class.
"""
import os
import sys
import json
import tempfile
from pathlib import Path

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# pylint: disable=wrong-import-position
from tests.unit.test_base import BaseUnitTest
from src.common.config import Config


class TestConfig(BaseUnitTest):
    """Test the Config class."""

    def run(self):
        """Run all config tests."""
        self.test_config_creation()
        self.test_config_get()
        self.test_config_defaults()
        self.test_config_paths()
        return self.results

    def test_config_creation(self):
        """Test that Config can be instantiated."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                self.assert_not_none(
                    config, "config_creation", "Config object created successfully"
                )
                self.assert_isinstance(
                    config,
                    Config,
                    "config_type",
                    "Config is correct type"
                )
        except Exception as exc:
            self.add_result("config_creation", False, f"Failed to create Config: {exc}")

    def test_config_get(self):
        """Test getting configuration values."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))

                # Test getting QR settings
                qr_settings = config.get('qr_settings')
                self.assert_not_none(qr_settings, "config_get_qr_settings", "Got QR settings")

                # Test dot notation
                error_correction = config.get('qr_settings.error_correction')
                self.assert_not_none(
                    error_correction,
                    "config_get_dot_notation",
                    "Got value using dot notation"
                )

                # Test default value
                missing = config.get('nonexistent_key', 'default_value')
                self.assert_equal(
                    'default_value',
                    missing,
                    "config_get_default",
                    "Default value returned for missing key"
                )
        except Exception as exc:
            self.add_result("config_get", False, f"Config get failed: {exc}")

    def test_config_defaults(self):
        """Test that default configuration values are correct."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))

                qr_settings = config.get_qr_settings()
                self.assert_not_none(qr_settings, "config_defaults_qr", "QR settings exist")
                self.assert_in(
                    'version',
                    qr_settings,
                    "config_defaults_version",
                    "QR settings contain version"
                )
                self.assert_in(
                    'error_correction',
                    qr_settings,
                    "config_defaults_error_correction",
                    "QR settings contain error_correction"
                )

                output_dir = config.get('default_output_dir')
                self.assert_not_none(
                    output_dir, "config_defaults_output_dir", "Output dir setting exists"
                )
                self.assert_isinstance(
                    output_dir,
                    str,
                    "config_defaults_output_dir_type",
                    "Output dir is string"
                )
        except Exception as exc:
            self.add_result("config_defaults", False, f"Config defaults test failed: {exc}")

    def test_config_paths(self):
        """Test configuration path handling."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Create config to initialize directory structure
                Config(config_dir=Path(tmpdir))

                # Test that config directory was created
                config_dir = Path(tmpdir)
                self.assert_true(
                    config_dir.exists(),
                    "config_paths_dir_exists",
                    "Config directory exists"
                )

                # Test that subdirectories were created
                logs_dir = config_dir / "logs"
                output_dir = config_dir / "output"

                self.assert_true(
                    logs_dir.exists(),
                    "config_paths_logs_exists",
                    "Logs directory exists"
                )
                self.assert_true(
                    output_dir.exists(),
                    "config_paths_output_exists",
                    "Output directory exists"
                )

                # Test that config file was created
                config_file = config_dir / "config.json"
                self.assert_true(
                    config_file.exists(),
                    "config_paths_file_exists",
                    "Config file exists"
                )

                # Test that config file is valid JSON
                with open(config_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.assert_not_none(
                        data, "config_paths_valid_json", "Config file is valid JSON"
                    )
        except Exception as exc:
            self.add_result("config_paths", False, f"Config paths test failed: {exc}")
