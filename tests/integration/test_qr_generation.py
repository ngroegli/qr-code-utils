"""
Integration test for end-to-end QR code generation.
"""
import os
import sys
import tempfile
import subprocess

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# pylint: disable=wrong-import-position
from tests.integration.test_base import BaseIntegrationTest


class TestQRCodeGeneration(BaseIntegrationTest):
    """Test end-to-end QR code generation via CLI."""

    def run(self):
        """Run all integration tests."""
        self.test_url_qr_generation()
        self.test_text_qr_generation()
        self.test_phone_qr_generation()
        return self.results

    def test_url_qr_generation(self):
        """Test generating a URL QR code via command line."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_file = os.path.join(tmpdir, "test_url_qr.png")
                wrapper_script = os.path.join(project_root, "qr-utils.sh")

                # Run the qr-utils command
                result = subprocess.run(
                    [
                        wrapper_script,
                        "--output", output_file,
                        "url",
                        "--url", "https://example.com"
                    ],
                    capture_output=True,
                    text=True,
                    check=False
                )

                # Check if command succeeded
                if result.returncode == 0:
                    self.add_result(
                        "url_qr_command_success",
                        True,
                        "URL QR generation command succeeded"
                    )
                else:
                    self.add_result(
                        "url_qr_command_success",
                        False,
                        f"Command failed: {result.stderr}"
                    )
                    return

                # Check if file was created
                if os.path.exists(output_file):
                    self.add_result(
                        "url_qr_file_exists",
                        True,
                        "QR code file was created"
                    )

                    # Check if file is not empty
                    if os.path.getsize(output_file) > 0:
                        self.add_result(
                            "url_qr_file_not_empty",
                            True,
                            f"QR code file has size {os.path.getsize(output_file)} bytes"
                        )
                    else:
                        self.add_result(
                            "url_qr_file_not_empty",
                            False,
                            "QR code file is empty"
                        )
                else:
                    self.add_result(
                        "url_qr_file_exists",
                        False,
                        "QR code file was not created"
                    )
        except Exception as exc:
            self.add_result("url_qr_generation", False, f"Test failed: {exc}")

    def test_text_qr_generation(self):
        """Test generating a text QR code via command line."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_file = os.path.join(tmpdir, "test_text_qr.png")
                wrapper_script = os.path.join(project_root, "qr-utils.sh")

                result = subprocess.run(
                    [
                        wrapper_script,
                        "--output", output_file,
                        "text",
                        "--text", "Hello, World!"
                    ],
                    capture_output=True,
                    text=True,
                    check=False
                )

                if result.returncode == 0 and os.path.exists(output_file):
                    self.add_result(
                        "text_qr_generation",
                        True,
                        "Text QR code generated successfully"
                    )
                else:
                    self.add_result(
                        "text_qr_generation",
                        False,
                        f"Text QR generation failed: {result.stderr}"
                    )
        except Exception as exc:
            self.add_result("text_qr_generation", False, f"Test failed: {exc}")

    def test_phone_qr_generation(self):
        """Test generating a phone QR code via command line."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_file = os.path.join(tmpdir, "test_phone_qr.png")
                wrapper_script = os.path.join(project_root, "qr-utils.sh")

                result = subprocess.run(
                    [
                        wrapper_script,
                        "--output", output_file,
                        "phone",
                        "--phone", "+1234567890"
                    ],
                    capture_output=True,
                    text=True,
                    check=False
                )

                if result.returncode == 0 and os.path.exists(output_file):
                    self.add_result(
                        "phone_qr_generation",
                        True,
                        "Phone QR code generated successfully"
                    )
                else:
                    self.add_result(
                        "phone_qr_generation",
                        False,
                        f"Phone QR generation failed: {result.stderr}"
                    )
        except Exception as exc:
            self.add_result("phone_qr_generation", False, f"Test failed: {exc}")
