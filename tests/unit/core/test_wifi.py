"""
Unit tests for WiFi QR Generator.
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
from src.core.wifi import WiFiQRGenerator
from src.common.config import Config


class TestWiFiQRGenerator(BaseUnitTest):
    """Test the WiFi QR Generator."""

    def run(self):
        """Run all WiFi QR generator tests."""
        self.test_generator_creation()
        self.test_prepare_data()
        self.test_security_types()
        self.test_hidden_network()
        self.test_generate_qr()
        return self.results

    def test_generator_creation(self):
        """Test that WiFiQRGenerator can be instantiated."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = WiFiQRGenerator(config)
                self.assert_not_none(
                    generator,
                    "wifi_generator_creation",
                    "WiFiQRGenerator created successfully"
                )
                self.assert_isinstance(
                    generator,
                    WiFiQRGenerator,
                    "wifi_generator_type",
                    "Generator is correct type"
                )
        except Exception as exc:
            self.add_result("wifi_generator_creation", False, f"Failed: {exc}")

    def test_prepare_data(self):
        """Test WiFi data preparation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = WiFiQRGenerator(config)

                data = generator.prepare_data(
                    ssid="MyNetwork",
                    password="SecurePass123",
                    security="WPA"
                )
                self.assert_true(
                    data.startswith("WIFI:"),
                    "wifi_prepare_format",
                    "WiFi data has WIFI: prefix"
                )
                self.assert_in(
                    "MyNetwork",
                    data,
                    "wifi_prepare_ssid",
                    "SSID included in data"
                )
                self.assert_in(
                    "SecurePass123",
                    data,
                    "wifi_prepare_password",
                    "Password included in data"
                )
        except Exception as exc:
            self.add_result("wifi_prepare_data", False, f"Failed: {exc}")

    def test_security_types(self):
        """Test different security types."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = WiFiQRGenerator(config)

                # Test WPA
                data = generator.prepare_data(
                    ssid="TestNet",
                    password="pass123",
                    security="WPA"
                )
                self.assert_in(
                    "T:WPA",
                    data,
                    "wifi_security_wpa",
                    "WPA security type correct"
                )

                # Test WEP
                data = generator.prepare_data(
                    ssid="TestNet",
                    password="pass123",
                    security="WEP"
                )
                self.assert_in(
                    "T:WEP",
                    data,
                    "wifi_security_wep",
                    "WEP security type correct"
                )

                # Test no encryption
                data = generator.prepare_data(
                    ssid="TestNet",
                    password="",
                    security="nopass"
                )
                self.assert_in(
                    "T:nopass",
                    data,
                    "wifi_security_nopass",
                    "No password security type correct"
                )
        except Exception as exc:
            self.add_result("wifi_security_types", False, f"Failed: {exc}")

    def test_hidden_network(self):
        """Test hidden network flag."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = WiFiQRGenerator(config)

                # Test hidden network
                data = generator.prepare_data(
                    ssid="HiddenNet",
                    password="pass123",
                    security="WPA",
                    hidden=True
                )
                self.assert_in(
                    "H:true",
                    data,
                    "wifi_hidden_true",
                    "Hidden flag set correctly"
                )

                # Test visible network
                data = generator.prepare_data(
                    ssid="VisibleNet",
                    password="pass123",
                    security="WPA",
                    hidden=False
                )
                self.assert_true(
                    "H:false" in data or "H:" not in data,
                    "wifi_hidden_false",
                    "Visible network handled correctly"
                )
        except Exception as exc:
            self.add_result("wifi_hidden_network", False, f"Failed: {exc}")

    def test_generate_qr(self):
        """Test QR code generation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = WiFiQRGenerator(config)

                output_path = Path(tmpdir) / "test_wifi_qr.png"

                result = generator.generate(
                    ssid="TestNetwork",
                    password="TestPass123",
                    security="WPA",
                    output_path=str(output_path)
                )

                self.assert_true(
                    output_path.exists(),
                    "wifi_qr_file_created",
                    "QR code file was created"
                )

                self.assert_true(
                    output_path.stat().st_size > 0,
                    "wifi_qr_file_not_empty",
                    "QR code file is not empty"
                )

                self.assert_not_none(
                    result,
                    "wifi_generate_returns_path",
                    "Generate method returns path"
                )
        except Exception as exc:
            self.add_result("wifi_generate_qr", False, f"Failed: {exc}")
