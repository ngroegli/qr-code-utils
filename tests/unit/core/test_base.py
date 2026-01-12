"""
Unit tests for Base QR Generator.
"""
import os
import sys
import tempfile
from pathlib import Path

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# pylint: disable=wrong-import-position
from tests.unit.test_base import BaseUnitTest
from src.core.text import TextQRGenerator  # Use concrete implementation
from src.common.config import Config


class TestBaseQRGenerator(BaseUnitTest):
    """Test the Base QR Generator functionality."""

    def run(self):
        """Run all base QR generator tests."""
        self.test_generator_creation()
        self.test_qr_settings()
        self.test_file_naming()
        self.test_error_correction_levels()
        return self.results

    def test_generator_creation(self):
        """Test that QR generators can be instantiated."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = TextQRGenerator(config)  # Use concrete class
                self.assert_not_none(
                    generator,
                    "base_generator_creation",
                    "QR Generator created successfully"
                )
                self.assert_not_none(
                    generator.config,
                    "base_generator_has_config",
                    "Generator has config"
                )
                self.assert_not_none(
                    generator.logger,
                    "base_generator_has_logger",
                    "Generator has logger"
                )
        except Exception as exc:
            self.add_result("base_generator_creation", False, f"Failed: {exc}")

    def test_qr_settings(self):
        """Test QR settings are loaded correctly."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                TextQRGenerator(config)

                qr_settings = config.get('qr_settings')
                self.assert_not_none(
                    qr_settings,
                    "base_qr_settings_exist",
                    "QR settings exist in config"
                )
                self.assert_isinstance(
                    qr_settings,
                    dict,
                    "base_qr_settings_type",
                    "QR settings is a dictionary"
                )
                self.assert_in(
                    'version',
                    qr_settings,
                    "base_qr_has_version",
                    "QR settings contain version"
                )
                self.assert_in(
                    'error_correction',
                    qr_settings,
                    "base_qr_has_error_correction",
                    "QR settings contain error_correction"
                )
        except Exception as exc:
            self.add_result("base_qr_settings", False, f"Failed: {exc}")

    def test_file_naming(self):
        """Test file naming conventions."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                TextQRGenerator(config)

                # Check that output directory exists
                output_dir = config.get('default_output_dir')
                self.assert_not_none(
                    output_dir,
                    "base_output_dir_configured",
                    "Output directory is configured"
                )
        except Exception as exc:
            self.add_result("base_file_naming", False, f"Failed: {exc}")

    def test_error_correction_levels(self):
        """Test that error correction levels are valid."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                TextQRGenerator(config)

                qr_settings = config.get('qr_settings')
                error_correction = qr_settings.get('error_correction', 'M')

                # Valid error correction levels: L, M, Q, H
                valid_levels = ['L', 'M', 'Q', 'H']
                self.assert_in(
                    error_correction,
                    valid_levels,
                    "base_error_correction_valid",
                    f"Error correction level '{error_correction}' is valid"
                )
        except Exception as exc:
            self.add_result("base_error_correction_levels", False, f"Failed: {exc}")
