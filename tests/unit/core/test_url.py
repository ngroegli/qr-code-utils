"""
Unit tests for URL QR Generator.
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
from src.core.url import URLQRGenerator
from src.common.config import Config


class TestURLQRGenerator(BaseUnitTest):
    """Test the URL QR Generator."""

    def run(self):
        """Run all URL QR generator tests."""
        self.test_generator_creation()
        self.test_prepare_data()
        self.test_generate_qr()
        self.test_invalid_url()
        return self.results

    def test_generator_creation(self):
        """Test that URLQRGenerator can be instantiated."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = URLQRGenerator(config)
                self.assert_not_none(
                    generator,
                    "url_generator_creation",
                    "URLQRGenerator created successfully"
                )
                self.assert_isinstance(
                    generator,
                    URLQRGenerator,
                    "url_generator_type",
                    "Generator is correct type"
                )
        except Exception as exc:
            self.add_result("url_generator_creation", False, f"Failed to create generator: {exc}")

    def test_prepare_data(self):
        """Test URL data preparation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = URLQRGenerator(config)

                # Test simple URL
                url = "https://example.com"
                data = generator.prepare_data(url=url)
                self.assert_equal(
                    url,
                    data,
                    "url_prepare_simple",
                    "Simple URL prepared correctly"
                )

                # Test URL with parameters
                url_with_params = "https://example.com?param=value&foo=bar"
                data = generator.prepare_data(url=url_with_params)
                self.assert_equal(
                    url_with_params,
                    data,
                    "url_prepare_params",
                    "URL with parameters prepared correctly"
                )
        except Exception as exc:
            self.add_result("url_prepare_data", False, f"Data preparation failed: {exc}")

    def test_generate_qr(self):
        """Test QR code generation."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = URLQRGenerator(config)

                url = "https://example.com"
                output_path = Path(tmpdir) / "test_qr.png"

                result = generator.generate(url=url, output_path=str(output_path))

                self.assert_true(
                    output_path.exists(),
                    "url_qr_file_created",
                    "QR code file was created"
                )

                self.assert_true(
                    output_path.stat().st_size > 0,
                    "url_qr_file_not_empty",
                    "QR code file is not empty"
                )

                self.assert_not_none(
                    result,
                    "url_generate_returns_path",
                    "Generate method returns path"
                )
        except Exception as exc:
            self.add_result("url_generate_qr", False, f"QR generation failed: {exc}")

    def test_invalid_url(self):
        """Test handling of invalid URLs."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                config = Config(config_dir=Path(tmpdir))
                generator = URLQRGenerator(config)

                # Empty URL gets protocol prefix added
                data = generator.prepare_data(url="")
                self.assert_equal(
                    "https://",
                    data,
                    "url_empty_handled",
                    "Empty URL gets protocol prefix"
                )

                # URL without protocol gets https:// prefix
                data = generator.prepare_data(url="not-a-url")
                self.assert_equal(
                    "https://not-a-url",
                    data,
                    "url_invalid_format",
                    "URL without protocol gets https:// prefix"
                )

                # URL with http:// stays as is
                data = generator.prepare_data(url="http://example.com")
                self.assert_equal(
                    "http://example.com",
                    data,
                    "url_http_preserved",
                    "URL with http:// protocol preserved"
                )
        except Exception as exc:
            self.add_result("url_invalid", False, f"Invalid URL test failed: {exc}")
