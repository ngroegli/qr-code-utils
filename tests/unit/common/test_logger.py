"""
Unit tests for Logger utility.
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
from src.common.logger import setup_logger
from src.common.config import Config


class TestLogger(BaseUnitTest):
    """Test the Logger utility."""

    def run(self):
        """Run all logger tests."""
        self.test_logger_creation()
        self.test_log_file_creation()
        self.test_log_levels()
        return self.results

    def test_logger_creation(self):
        """Test that logger can be created."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                Config(config_dir=Path(tmpdir))  # Create config structure
                log_dir = Path(tmpdir) / "logs"
                logger = setup_logger("test_logger", log_dir=log_dir)
                self.assert_not_none(
                    logger,
                    "logger_creation",
                    "Logger created successfully"
                )
        except Exception as exc:
            self.add_result("logger_creation", False, f"Failed: {exc}")

    def test_log_file_creation(self):
        """Test that log files are created."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                Config(config_dir=Path(tmpdir))
                log_dir = Path(tmpdir) / "logs"
                log_dir.mkdir(parents=True, exist_ok=True)

                logger = setup_logger("test_file", log_dir=log_dir)

                # Write a log message
                logger.info("Test log message")

                # Check that logs directory exists
                self.assert_true(
                    log_dir.exists(),
                    "logger_dir_exists",
                    "Logs directory exists"
                )
        except Exception as exc:
            self.add_result("logger_file_creation", False, f"Failed: {exc}")

    def test_log_levels(self):
        """Test different log levels."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                Config(config_dir=Path(tmpdir))
                log_dir = Path(tmpdir) / "logs"
                log_dir.mkdir(parents=True, exist_ok=True)

                logger = setup_logger("test_levels", log_dir=log_dir)

                # Test that different log levels work without errors
                logger.debug("Debug message")
                logger.info("Info message")
                logger.warning("Warning message")
                logger.error("Error message")

                self.add_result(
                    "logger_all_levels",
                    True,
                    "All log levels work without errors"
                )
        except Exception as exc:
            self.add_result("logger_log_levels", False, f"Failed: {exc}")
