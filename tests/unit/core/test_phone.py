"""
Unit tests for Phone QR Generator.
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
from src.core.phone import PhoneQRGenerator
from src.common.config import Config


class TestPhoneQRGenerator(BaseUnitTest):
    """Test the Phone QR Generator."""

    def run(self):
        """Run all Phone QR generator tests."""
        self.test_generator_creation()
        self.test_prepare_data()
        self.test_phone_formats()
        self.test_generate_qr()
        return self.results

    def test_generator_creation(self):
        """Test that PhoneQRGenerator can be instantiated."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = PhoneQRGenerator(config)
                self.assert_not_none(
                    generator,
                    "phone_generator_creation",
                    "PhoneQRGenerator created successfully"
                )
                self.assert_isinstance(
                    generator,
                    PhoneQRGenerator,
                    "phone_generator_type",
                    "Generator is correct type"
                )
        except Exception as exc:
            self.add_result("phone_generator_creation", False, f"Failed: {exc}")

    def test_prepare_data(self):
        """Test phone data preparation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = PhoneQRGenerator(config)

                phone = "+1234567890"
                data = generator.prepare_data(phone_number=phone)
                self.assert_true(
                    data.startswith("tel:"),
                    "phone_prepare_format",
                    "Phone data has tel: prefix"
                )
                self.assert_in(
                    phone,
                    data,
                    "phone_prepare_number",
                    "Phone number included in data"
                )
        except Exception as exc:
            self.add_result("phone_prepare_data", False, f"Failed: {exc}")

    def test_phone_formats(self):
        """Test various phone number formats."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = PhoneQRGenerator(config)

                # Test with country code
                data = generator.prepare_data(phone_number="+1-555-123-4567")
                self.assert_true(
                    "tel:" in data,
                    "phone_format_international",
                    "International format handled"
                )

                # Test simple number
                data = generator.prepare_data(phone_number="5551234567")
                self.assert_true(
                    "tel:" in data,
                    "phone_format_simple",
                    "Simple format handled"
                )
        except Exception as exc:
            self.add_result("phone_formats", False, f"Failed: {exc}")

    def test_generate_qr(self):
        """Test QR code generation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = PhoneQRGenerator(config)

                phone = "+1234567890"
                output_path = Path(tmpdir) / "test_phone_qr.png"

                result = generator.generate(
                    phone_number=phone, output_path=str(output_path)
                )

                self.assert_true(
                    output_path.exists(),
                    "phone_qr_file_created",
                    "QR code file was created"
                )

                self.assert_true(
                    output_path.stat().st_size > 0,
                    "phone_qr_file_not_empty",
                    "QR code file is not empty"
                )

                self.assert_not_none(
                    result,
                    "phone_generate_returns_path",
                    "Generate method returns path"
                )
        except Exception as exc:
            self.add_result("phone_generate_qr", False, f"Failed: {exc}")
