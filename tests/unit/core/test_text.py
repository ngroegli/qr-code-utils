"""
Unit tests for Text QR Generator.
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
from src.core.text import TextQRGenerator
from src.common.config import Config


class TestTextQRGenerator(BaseUnitTest):
    """Test the Text QR Generator."""

    def run(self):
        """Run all Text QR generator tests."""
        self.test_generator_creation()
        self.test_prepare_data()
        self.test_generate_qr()
        self.test_multiline_text()
        self.test_special_characters()
        return self.results

    def test_generator_creation(self):
        """Test that TextQRGenerator can be instantiated."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = TextQRGenerator(config)
                self.assert_not_none(
                    generator,
                    "text_generator_creation",
                    "TextQRGenerator created successfully"
                )
                self.assert_isinstance(
                    generator,
                    TextQRGenerator,
                    "text_generator_type",
                    "Generator is correct type"
                )
        except Exception as exc:
            self.add_result("text_generator_creation", False, f"Failed: {exc}")

    def test_prepare_data(self):
        """Test text data preparation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = TextQRGenerator(config)

                text = "Hello, World!"
                data = generator.prepare_data(text=text)
                self.assert_equal(
                    text,
                    data,
                    "text_prepare_simple",
                    "Simple text prepared correctly"
                )
        except Exception as exc:
            self.add_result("text_prepare_data", False, f"Failed: {exc}")

    def test_generate_qr(self):
        """Test QR code generation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = TextQRGenerator(config)

                text = "Test message"
                output_path = Path(tmpdir) / "test_text_qr.png"

                result = generator.generate(text=text, output_path=str(output_path))

                self.assert_true(
                    output_path.exists(),
                    "text_qr_file_created",
                    "QR code file was created"
                )

                self.assert_true(
                    output_path.stat().st_size > 0,
                    "text_qr_file_not_empty",
                    "QR code file is not empty"
                )

                self.assert_not_none(
                    result,
                    "text_generate_returns_path",
                    "Generate method returns path"
                )
        except Exception as exc:
            self.add_result("text_generate_qr", False, f"Failed: {exc}")

    def test_multiline_text(self):
        """Test multiline text handling."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = TextQRGenerator(config)

                text = "Line 1\nLine 2\nLine 3"
                data = generator.prepare_data(text=text)
                self.assert_equal(
                    text,
                    data,
                    "text_multiline",
                    "Multiline text preserved"
                )
        except Exception as exc:
            self.add_result("text_multiline", False, f"Failed: {exc}")

    def test_special_characters(self):
        """Test special characters handling."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = TextQRGenerator(config)

                # Test with emojis and special characters
                text = "Hello 👋 & Welcome! @#$%"
                data = generator.prepare_data(text=text)
                self.assert_equal(
                    text,
                    data,
                    "text_special_chars",
                    "Special characters preserved"
                )
        except Exception as exc:
            self.add_result("text_special_chars", False, f"Failed: {exc}")
