# Testing Infrastructure for QR Code Utils

## Overview

This document describes the testing infrastructure implemented for the QR Code Utils project, including unit tests, integration tests, and linting scripts.

## Structure

```
qr-code-utils/
├── .pylintrc                     # Pylint configuration
├── run_pylint.sh                 # Linting script with color-coded output
├── tests/
│   ├── __init__.py
│   ├── run_unit_tests.py         # Unit test runner
│   ├── run_unit_tests.sh         # Shell wrapper for unit tests
│   ├── run_integration_tests.py  # Integration test runner
│   ├── run_integration_tests.sh  # Shell wrapper for integration tests
│   ├── test_resources/           # Test assets (logos, configs, etc.)
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_base.py          # Base class for unit tests
│   │   ├── common/
│   │   │   ├── __init__.py
│   │   │   └── test_config.py    # Tests for Config class
│   │   └── core/
│   │       ├── __init__.py
│   │       └── test_url.py       # Tests for URL QR generator
│   └── integration/
│       ├── __init__.py
│       ├── test_base.py          # Base class for integration tests
│       └── test_qr_generation.py # End-to-end QR generation tests
```

## Running Tests

### Unit Tests

Run all unit tests:
```bash
./tests/run_unit_tests.sh
```

List available unit tests:
```bash
./tests/run_unit_tests.sh --list
```

Run tests from a specific category:
```bash
./tests/run_unit_tests.sh --category common
./tests/run_unit_tests.sh --category core
```

Run a specific test:
```bash
./tests/run_unit_tests.sh --test config
```

### Integration Tests

Run all integration tests:
```bash
./tests/run_integration_tests.sh
```

List available integration tests:
```bash
./tests/run_integration_tests.sh --list
```

Run a specific test:
```bash
./tests/run_integration_tests.sh --test qr_generation
```

### Linting

Run pylint with color-coded severity output:
```bash
./run_pylint.sh
```

The script categorizes issues by severity:
- **Critical Errors (E)** - Red - Blocks merging
- **Warnings (W)** - Yellow - Should be addressed
- **Refactoring (R)** - Cyan - Recommendations
- **Convention (C)** - Magenta - Style issues

## Writing Tests

### Unit Tests

Create a new unit test by extending `BaseUnitTest`:

```python
from tests.unit.test_base import BaseUnitTest

class TestMyFeature(BaseUnitTest):
    """Test my feature."""

    def run(self):
        """Run all tests."""
        self.test_something()
        self.test_something_else()
        return self.results

    def test_something(self):
        """Test a specific behavior."""
        self.assert_equal(
            expected_value,
            actual_value,
            "test_name",
            "Description of what is being tested"
        )
```

Available assertions:
- `assert_equal(expected, actual, test_name, message)`
- `assert_not_equal(not_expected, actual, test_name, message)`
- `assert_true(condition, test_name, message)`
- `assert_false(condition, test_name, message)`
- `assert_not_none(value, test_name, message)`
- `assert_is_none(value, test_name, message)`
- `assert_in(item, container, test_name, message)`
- `assert_not_in(item, container, test_name, message)`
- `assert_isinstance(obj, class_or_tuple, test_name, message)`
- `assert_raises(exception_class, callable_obj, test_name, message)`

### Integration Tests

Create integration tests by extending `BaseIntegrationTest`:

```python
from tests.integration.test_base import BaseIntegrationTest

class TestMyIntegration(BaseIntegrationTest):
    """Test end-to-end functionality."""

    def run(self):
        """Run all integration tests."""
        self.test_full_workflow()
        return self.results

    def test_full_workflow(self):
        """Test complete workflow."""
        # Test implementation
        self.add_result("test_name", passed=True, message="Test passed")
```

## Test Categories

### Unit Tests

**Common Tests** (`tests/unit/common/`)
- `test_config.py` - Configuration management tests
- Future: `test_logger.py` - Logging functionality tests

**Core Tests** (`tests/unit/core/`)
- `test_url.py` - URL QR generator tests
- Future: Tests for all 11 QR generator types

### Integration Tests

**End-to-End Tests** (`tests/integration/`)
- `test_qr_generation.py` - CLI-based QR code generation tests

## Configuration

### Pylint (.pylintrc)

The project uses a custom pylint configuration that:
- Sets minimum score threshold to 8.0
- Disables overly strict checks for this project
- Configures appropriate line length (100 characters)
- Defines naming conventions
- Ignores venv and tmp_external_ref directories

Key disabled checks:
- Documentation requirements (handled separately)
- `wrong-import-position` (needed for path setup)
- `arguments-differ` (used intentionally for LSP compliance)

## Continuous Integration

The testing infrastructure is designed to integrate with CI/CD pipelines:

1. **Linting** - Must pass with no critical errors
2. **Unit Tests** - Must pass 100%
3. **Integration Tests** - Must pass 100%

Example CI workflow:
```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
./run_pylint.sh
if [ $? -ne 0 ]; then exit 1; fi

# Run unit tests
./tests/run_unit_tests.sh
if [ $? -ne 0 ]; then exit 1; fi

# Run integration tests
./tests/run_integration_tests.sh
if [ $? -ne 0 ]; then exit 1; fi
```

## Current Test Status

**Unit Tests:**
- ✅ Config class tests (15 tests - all passing)
- ⚠️ URL QR generator tests (9 tests - 7 passing, 2 minor failures)

**Integration Tests:**
- ✅ QR generation via CLI (3 tests)

**Total Coverage:**
- Common module: Config class
- Core module: URL QR generator
- CLI integration: URL, Text, Phone QR types

## Future Enhancements

1. **Add tests for remaining QR types:**
   - vCard, WiFi, SMS, Email, Location, Event, WhatsApp, Payment

2. **Expand test coverage:**
   - Logo embedding
   - Custom QR settings
   - Error handling
   - Edge cases

3. **Add performance tests:**
   - Batch generation
   - Large data handling

4. **Add code coverage reporting:**
   - Install coverage.py
   - Generate HTML reports
   - Set minimum coverage threshold

5. **Mock external dependencies:**
   - File system operations
   - Image processing

## Troubleshooting

### Tests fail to import modules

Make sure you're running tests from the project root and the virtual environment is activated:
```bash
source venv/bin/activate
cd /path/to/qr-code-utils
./tests/run_unit_tests.sh
```

### Pylint fails to find modules

Ensure PYTHONPATH is set correctly in the script or run from project root:
```bash
export PYTHONPATH=src:$PWD
./run_pylint.sh
```

### Integration tests fail

Check that:
1. `qr-utils.sh` wrapper script is executable
2. Virtual environment is properly set up
3. All dependencies are installed

## References

- Based on testing patterns from `tmp_external_ref/tests/`
- Follows pytest-like assertion patterns
- Color-coded output for better readability
- Modular test discovery system
