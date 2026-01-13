# GitHub Workflows Summary

This document summarizes the GitHub Actions workflows configured for the qr-code-utils project.

## Overview

All workflows have been aligned with the project structure and requirements. The workflows were originally copied from another project (which had Docker containerization and Python package distribution) and have been simplified to match this script-based QR code toolkit.

## Workflow Files

### 1. `ci.yml` - Continuous Integration
**Triggers:** Pull requests to main/develop, pushes to main/develop, manual trigger

**Purpose:** Validates code quality and tests on every code change

**Jobs:**
- **validate-and-test**: Runs code quality checks and all tests
  - Pylint code quality analysis (must achieve 10.00/10 score)
  - Unit tests (67 tests via `python tests/run_unit_tests.py`)
  - Integration tests (5 tests via `python tests/run_integration_tests.py`)
  - Uses custom test runners (not pytest)

**Key Features:**
- Parses custom test runner output format (looks for "OVERALL SUMMARY")
- Fails workflow if pylint score < 10.00 or any test fails
- Generates GitHub step summary with test results

---

### 2. `release.yml` - Release Workflow
**Triggers:** Version tags (v*), manual trigger with version input

**Purpose:** Creates GitHub releases when version tags are pushed

**Jobs:**
1. **validate-and-test**: Validates release before creating it
   - Extracts version from tag or manual input
   - Detects if pre-release (contains alpha/beta/rc)
   - Runs pylint checks (10.00/10 required)
   - Runs all unit and integration tests
   - Sets outputs: version, tag_version, is_prerelease

2. **create-release**: Creates the GitHub release
   - Generates release notes with commit history
   - Creates GitHub release with proper metadata
   - Marks as pre-release if version contains alpha/beta/rc
   - Adds installation instructions to release notes

**Changes from Original:**
- ❌ Removed: Docker image building and pushing
- ❌ Removed: Python package building and PyPI publishing
- ❌ Removed: References to non-existent scripts (validate_version.py, bump_version.py)
- ✅ Added: Simplified version extraction from git tags
- ✅ Added: Custom test runner integration
- ✅ Added: Pre-release detection logic

**Release Process:**
```bash
# Create and push a version tag to trigger release
git tag -a v2.0.1 -m "Release version 2.0.1"
git push origin v2.0.1

# Or trigger manually from GitHub Actions UI
# Actions → Release → Run workflow → Enter version
```

---

### 3. `pylint.yml` - Standalone Pylint Analysis
**Triggers:** Manual trigger, weekly schedule (Sundays at 2 AM UTC)

**Purpose:** Detailed code quality analysis for monitoring

**Jobs:**
- **lint**: Comprehensive pylint analysis by severity
  - Runs full pylint with .pylintrc configuration
  - Breaks down issues by category: Errors (E), Warnings (W), Refactoring (R), Conventions (C), Information (I)
  - Respects disabled checks from .pylintrc
  - Only fails on critical errors (E category)
  - Generates detailed GitHub step summary

**Key Features:**
- Uses same logic as `run_pylint.sh` script
- Color-coded severity categories
- Explains pylint exit codes
- Perfect for periodic code quality monitoring

---

### 4. `security.yml` - Security Scanning
**Triggers:** Weekly schedule (Mondays at 2 AM UTC), pushes to main/develop, pull requests, manual trigger

**Purpose:** Comprehensive security scanning of dependencies and code

**Jobs:**
1. **dependency-scanning**: Scans for known vulnerabilities
   - Uses `safety` tool to check dependencies
   - Generates JSON and text reports
   - Uploads reports as artifacts (30-day retention)

2. **code-security-scan**: Analyzes code for security issues
   - Uses `bandit` to find security vulnerabilities
   - Skips B110, B112 (pass/tryexcept checks)
   - Medium severity threshold
   - Uploads reports as artifacts

3. **secret-scanning**: Detects leaked secrets
   - Uses `gitleaks` to scan git history
   - Checks for API keys, tokens, credentials

4. **codeql-analysis**: Advanced security analysis
   - GitHub's CodeQL static analysis
   - Security and quality queries
   - Results appear in Security tab

5. **security-summary**: Aggregates all scan results
   - Downloads all security reports
   - Generates summary in GitHub step summary
   - Fails if critical issues found (>5 vulnerabilities or any high-severity issues)

**Changes from Original:**
- ❌ Removed: Container security scanning (Docker Trivy)
- ✅ Kept: All relevant security scans for Python code

---

## Workflow Dependencies

```
CI Workflow (ci.yml)
└── validate-and-test
    ├── Pylint (10.00/10 required)
    ├── Unit Tests (67 tests)
    └── Integration Tests (5 tests)

Release Workflow (release.yml)
├── validate-and-test
│   ├── Extract version
│   ├── Pylint (10.00/10)
│   ├── Unit Tests
│   └── Integration Tests
└── create-release (depends on validate-and-test)
    ├── Generate release notes
    └── Create GitHub release

Pylint Workflow (pylint.yml)
└── lint
    ├── Full pylint analysis
    └── Severity breakdown

Security Workflow (security.yml)
├── dependency-scanning (Safety)
├── code-security-scan (Bandit)
├── secret-scanning (Gitleaks)
├── codeql-analysis (GitHub CodeQL)
└── security-summary (depends on all above)
```

---

## Environment Variables

All workflows use:
- `PYTHONPATH`: Set to `src` or `$GITHUB_WORKSPACE/src` for proper module imports
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- Python 3.12: Standard version for all jobs

---

## Test Execution

### Custom Test Runners (Not pytest!)

The project uses custom test runners with dynamic discovery:

```bash
# Unit tests (67 tests)
export PYTHONPATH="$GITHUB_WORKSPACE/src"
python tests/run_unit_tests.py

# Integration tests (5 tests)
export PYTHONPATH="$GITHUB_WORKSPACE/src"
python tests/run_integration_tests.py
```

**Output Format:**
```
=== OVERALL SUMMARY ===
Total Tests Run: 67
Passed: 67
Failed: 0
```

The CI workflow parses this format to extract test results.

---

## Code Quality Requirements

### Pylint Score: 10.00/10

All code must maintain a perfect pylint score:
- Uses `.pylintrc` for configuration
- Custom disabled checks for project-specific needs
- Script: `./run_pylint.sh` provides color-coded output

### Test Coverage: 100% Pass Rate

Currently:
- ✅ 67 unit tests (all passing)
- ✅ 5 integration tests (all passing)
- ✅ 72 total tests

---

## Artifacts and Reports

### CI Workflow
- Test results in GitHub step summary
- Pylint score in step summary

### Release Workflow
- GitHub releases with:
  - Release notes
  - Commit history
  - Installation instructions
  - Pre-release flag (if applicable)

### Security Workflow (30-day retention)
- `safety-vulnerability-report`: JSON report of dependency vulnerabilities
- `bandit-security-report`: JSON report of code security issues
- CodeQL results in Security tab → Code scanning alerts

---

## Backup Files

Original workflows from the copied project are preserved:
- `.github/workflows/release.yml.bak` (original 367-line version)

These can be referenced if needed but should not be used directly as they contain Docker and PyPI-specific steps not applicable to this project.

---

## Project-Specific Notes

### This is NOT:
- ❌ A containerized application (no Docker)
- ❌ A Python package (no PyPI distribution)
- ❌ Using pytest (custom test runners)
- ❌ Using automated version management scripts

### This IS:
- ✅ A script-based CLI toolkit (`./qr-utils.sh`)
- ✅ Using custom test discovery and runners
- ✅ Using git tags for version management
- ✅ Simple GitHub releases (tags + notes)
- ✅ Maintaining 10.00/10 pylint score

---

## Quick Reference

### Run Tests Locally
```bash
export PYTHONPATH="$(pwd)/src"
python tests/run_unit_tests.py
python tests/run_integration_tests.py
```

### Run Linting Locally
```bash
./run_pylint.sh
```

### Create a Release
```bash
# Create tag
git tag -a v2.0.1 -m "Release version 2.0.1"
git push origin v2.0.1

# GitHub Actions will automatically:
# 1. Run all tests
# 2. Validate code quality
# 3. Create GitHub release
```

### Trigger Workflows Manually
- Go to Actions tab in GitHub
- Select workflow (CI, Release, Pylint, or Security)
- Click "Run workflow"
- Fill in required inputs (if any)

---

## Status Badges

Add these to README.md for workflow status visibility:

```markdown
[![CI](https://github.com/YOUR_USERNAME/qr-code-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/qr-code-utils/actions/workflows/ci.yml)
[![Pylint](https://github.com/YOUR_USERNAME/qr-code-utils/actions/workflows/pylint.yml/badge.svg)](https://github.com/YOUR_USERNAME/qr-code-utils/actions/workflows/pylint.yml)
[![Security](https://github.com/YOUR_USERNAME/qr-code-utils/actions/workflows/security.yml/badge.svg)](https://github.com/YOUR_USERNAME/qr-code-utils/actions/workflows/security.yml)
```

---

**Last Updated:** January 13, 2025  
**Workflows Version:** Aligned with qr-code-utils v2.0.0
