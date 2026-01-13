# Release Guide

**Version:** 1.0
**Last Updated:** January 13, 2025

This document provides comprehensive guidance for creating and managing releases of the QR Code Utils project.

---

## Table of Contents

1. [Versioning Strategy](#versioning-strategy)
2. [Release Process](#release-process)
3. [Pre-Release Checklist](#pre-release-checklist)
4. [Creating a Release](#creating-a-release)
5. [CI/CD Workflows](#cicd-workflows)
6. [Hotfix Releases](#hotfix-releases)
7. [Release Notes Guidelines](#release-notes-guidelines)
8. [Troubleshooting](#troubleshooting)

---

## Versioning Strategy

### Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH[-PRERELEASE]
```

**Examples:**
- `1.0.0` - Initial stable release
- `1.1.0` - New features added (backward compatible)
- `1.0.1` - Bug fixes only
- `2.0.0` - Breaking changes
- `1.2.0-alpha.1` - Pre-release version
- `1.2.0-beta.1` - Beta release
- `1.2.0-rc.1` - Release candidate

### Version Components

#### MAJOR version (X.0.0)
Increment when you make incompatible API changes or breaking changes:
- Changing CLI argument names
- Removing generators or major features
- Changing output file structure
- Python version requirements change

#### MINOR version (1.X.0)
Increment when you add functionality in a backward-compatible manner:
- Adding new QR code generator types
- Adding new CLI options (backward compatible)
- Adding new features to existing generators
- Performance improvements

#### PATCH version (1.0.X)
Increment when you make backward-compatible bug fixes:
- Fixing incorrect QR code generation
- Fixing logging issues
- Fixing configuration bugs
- Documentation fixes
- Security patches

#### Pre-release versions
Format: `X.Y.Z-identifier.N`
- `alpha` - Early development, unstable
- `beta` - Feature complete, testing phase
- `rc` (release candidate) - Ready for release, final testing

---

## Release Process

### Overview

```
1. Code & Test → 2. Version Decision → 3. Pre-Release Checks → 4. Create Tag → 5. CI/CD → 6. Publish
```

### Step-by-Step Guide

#### Step 1: Ensure Code Quality

Before starting a release:

```bash
# Run all linting checks
./run_pylint.sh

# Run all tests
export PYTHONPATH="$(pwd)/src"
python tests/run_unit_tests.py
python tests/run_integration_tests.py
```

**Requirements:**
- ✅ Pylint score: **10.00/10**
- ✅ Unit tests: **All 67 passing**
- ✅ Integration tests: **All passing locally**
- ✅ No critical security vulnerabilities

#### Step 2: Update Documentation

- Update version numbers if needed in docs
- Review and update `README.md` if features changed
- Ensure all new features are documented

#### Step 3: Commit All Changes

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "chore: prepare for v1.X.X release

- Updated documentation
- Fixed minor issues
- Ready for release"

# Push to GitHub
git push origin main
```

#### Step 4: Wait for CI to Pass

After pushing, check GitHub Actions:
- Go to: `https://github.com/ngroegli/qr-code-utils/actions`
- Wait for **Continuous Integration** workflow to complete
- Ensure all jobs pass (pylint + tests)

#### Step 5: Create Release Tag

Once CI passes:

```bash
# Determine version number (e.g., v1.0.1)
VERSION="v1.0.1"

# Create annotated tag with release notes
git tag -a $VERSION -m "Release version $VERSION

**What's New:**
- Fixed XYZ bug in WiFi generator
- Improved error handling in config module
- Updated documentation

**Bug Fixes:**
- Issue #123: QR code generation fails with special characters
- Issue #124: Logger not creating log directory

All tests passing (67 unit tests) with 10.00/10 pylint score."

# Push the tag to GitHub
git push origin $VERSION
```

#### Step 6: Release Workflow Triggers

The GitHub Actions release workflow automatically:
1. ✅ Validates the version tag
2. ✅ Runs pylint (must be 10.00/10)
3. ✅ Runs all 67 unit tests
4. ✅ Generates release notes from commits
5. ✅ Creates GitHub release with:
   - Tag reference
   - Release notes
   - Installation instructions
   - Changelog from git commits
   - Pre-release flag (if applicable)

#### Step 7: Verify Release

- Check: `https://github.com/ngroegli/qr-code-utils/releases`
- Verify release notes are correct
- Test installation instructions
- Announce release (if needed)

---

## Pre-Release Checklist

Use this checklist before creating any release:

### Code Quality
- [ ] Pylint score is 10.00/10
- [ ] All unit tests pass (67/67)
- [ ] Integration tests pass locally
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] No unused imports

### Documentation
- [ ] CHANGELOG.md updated
- [ ] README.md reflects current features
- [ ] All new features documented
- [ ] API changes documented
- [ ] Code examples tested

### Testing
- [ ] New features have unit tests
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] CLI arguments validated

### Security
- [ ] No hardcoded credentials
- [ ] Dependencies up to date
- [ ] Security scan passed
- [ ] No known vulnerabilities

### Git
- [ ] All changes committed
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] CI/CD passes on GitHub

---

## Creating a Release

### Standard Release (Stable)

For stable production releases:

```bash
# Example: v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0

New Features:
- Added PaymentQRGenerator for payment QR codes
- Added WhatsAppQRGenerator for WhatsApp links
- Improved error messages

Bug Fixes:
- Fixed WiFi special character escaping
- Fixed vCard formatting issues

All tests passing with 10.00/10 pylint score."

git push origin v1.2.0
```

### Pre-Release (Alpha/Beta/RC)

For testing and early access:

```bash
# Alpha release (early development)
git tag -a v1.3.0-alpha.1 -m "Release v1.3.0-alpha.1 (Pre-Release)

Early preview of upcoming features:
- Experimental calendar event generator
- New configuration options

⚠️ This is an alpha release. Not recommended for production."

# Beta release (feature complete, testing)
git tag -a v1.3.0-beta.1 -m "Release v1.3.0-beta.1 (Pre-Release)

Feature complete, ready for testing:
- Calendar event generator
- Enhanced configuration management

Please test and report issues."

# Release candidate (final testing)
git tag -a v1.3.0-rc.1 -m "Release v1.3.0-rc.1 (Release Candidate)

Final candidate for v1.3.0:
- All features complete and tested
- Documentation updated
- Ready for production use

Final testing phase before stable release."

git push origin v1.3.0-rc.1
```

The workflow automatically detects pre-releases and marks them accordingly on GitHub.

### Patch Release (Bug Fix)

For bug fixes only:

```bash
git tag -a v1.0.2 -m "Release version 1.0.2

Bug Fixes:
- Fixed: URL normalization handles edge cases correctly
- Fixed: Config directory creation on Windows
- Fixed: Logger rotation for large log files

All tests passing with 10.00/10 pylint score."

git push origin v1.0.2
```

---

## CI/CD Workflows

### Workflow Overview

The project uses GitHub Actions for continuous integration and deployment:

```
┌─────────────────┐
│  Push to main   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   CI Workflow   │  Runs on every push/PR
│  - Pylint check │  - Must score 10.00/10
│  - Unit tests   │  - All 67 tests must pass
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Push vX.Y.Z   │
│      tag        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Release Workflow│  Triggered by version tags
│  - Validate     │  - Runs all checks again
│  - Test         │  - Generates release notes
│  - Create       │  - Publishes to GitHub
│    Release      │
└─────────────────┘
```

### CI Workflow (`ci.yml`)

**Triggers:**
- Push to `main`
- Pull requests to `main`
- Manual trigger

**Jobs:**
1. **Pylint Check** - Code quality (10.00/10 required)
2. **Unit Tests** - Run all 67 unit tests
3. **Summary** - Overall CI status

**Requirements:**
- Python 3.12
- All dependencies from `requirements.txt`
- PYTHONPATH set to `src/`

### Release Workflow (`release.yml`)

**Triggers:**
- Tags matching `v*` pattern (e.g., `v1.0.0`)
- Manual trigger with version input

**Jobs:**
1. **validate-and-test**
   - Extract version from tag
   - Detect pre-release (alpha/beta/rc)
   - Run pylint (10.00/10)
   - Run unit tests (67 tests)

2. **create-release**
   - Generate release notes
   - Include commit history
   - Add installation instructions
   - Create GitHub release
   - Mark as pre-release if applicable

**Outputs:**
- GitHub release at: `https://github.com/ngroegli/qr-code-utils/releases`

### Security Workflow (`security.yml`)

**Triggers:**
- Weekly schedule (Mondays at 2 AM UTC)
- Push to `main`
- Pull requests to `main`

**Jobs:**
- Dependency scanning (Safety)
- Code security analysis (Bandit)
- Secret detection (Gitleaks)
- CodeQL analysis

### Pylint Workflow (`pylint.yml`)

**Triggers:**
- Weekly schedule (Sundays at 2 AM UTC)
- Manual trigger

**Purpose:**
- Detailed code quality monitoring
- Severity breakdown (Errors, Warnings, Refactoring, Conventions)
- Only fails on critical errors

---

## Hotfix Releases

For critical bugs that need immediate fixes:

### Process

1. **Create hotfix branch** (optional, can work on main)
   ```bash
   git checkout -b hotfix/v1.0.2
   ```

2. **Fix the critical issue**
   - Make minimal changes
   - Focus only on the critical bug
   - Add test for the fix

3. **Test thoroughly**
   ```bash
   ./run_pylint.sh
   python tests/run_unit_tests.py
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "fix: critical bug in WiFi generator

Fixes issue where special characters caused QR generation to fail.

Resolves #126"
   git push origin main  # or merge hotfix branch
   ```

5. **Create patch release immediately**
   ```bash
   git tag -a v1.0.2 -m "Hotfix Release v1.0.2

Critical Fix:
- Fixed WiFi QR generator crash with special characters

This is a critical bug fix release. All users should update immediately."
   git push origin v1.0.2
   ```

6. **Announce hotfix**
   - Update release notes
   - Notify users if critical

---

## Release Notes Guidelines

### Structure

```markdown
## Release vX.Y.Z - YYYY-MM-DD

### 🎉 New Features
- Feature 1: Description
- Feature 2: Description

### 🐛 Bug Fixes
- Fixed: Issue description
- Fixed: Another issue

### 🔧 Improvements
- Improved: Performance enhancement
- Improved: Better error messages

### ⚠️ Breaking Changes (for major releases)
- Changed: Old behavior → New behavior
- Removed: Feature that was deprecated

### 📚 Documentation
- Updated: Guide improvements
- Added: New examples

### 🔒 Security
- Fixed: Security vulnerability description

### ⬆️ Dependencies
- Updated: package@version
- Added: new-package@version
```

### Tips

- **Be specific**: "Fixed URL validation" vs "Fixed bug"
- **Include issue numbers**: "Fixes #123"
- **Explain impact**: Who is affected and why they should care
- **Use emojis**: Makes releases more scannable
- **Link to commits**: Use commit hashes for technical details

---

## Troubleshooting

### Release Workflow Fails

**Problem:** Tests fail during release workflow

**Solution:**
1. Check GitHub Actions logs
2. Run tests locally: `python tests/run_unit_tests.py`
3. Fix failures
4. Delete the tag: `git tag -d v1.0.1 && git push origin :refs/tags/v1.0.1`
5. Create new tag after fixes

### Pylint Score Not 10.00/10

**Problem:** Release fails due to pylint score

**Solution:**
```bash
# Run pylint locally
./run_pylint.sh

# Fix all issues
# Re-run until 10.00/10

# Then create release
```

### Wrong Version Tagged

**Problem:** Created tag with wrong version number

**Solution:**
```bash
# Delete local tag
git tag -d v1.0.1

# Delete remote tag
git push origin :refs/tags/v1.0.1

# Create correct tag
git tag -a v1.0.2 -m "Release version 1.0.2"
git push origin v1.0.2
```

### Release Not Appearing

**Problem:** Pushed tag but no release created

**Solution:**
1. Check GitHub Actions: `https://github.com/ngroegli/qr-code-utils/actions/workflows/release.yml`
2. Check workflow logs for errors
3. Verify tag format: `v` prefix required (e.g., `v1.0.0`)
4. Check GitHub permissions

### Pre-Release Marked as Stable

**Problem:** Beta release marked as stable

**Solution:**
- Tag must contain `alpha`, `beta`, or `rc` in version
- Example: `v1.2.0-beta.1` (correctly marked as pre-release)
- Example: `v1.2.0-test` (incorrectly marked as stable)

---

## Quick Reference

### Commands Cheatsheet

```bash
# Check code quality
./run_pylint.sh

# Run tests
export PYTHONPATH="$(pwd)/src"
python tests/run_unit_tests.py

# Create release tag
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1

# Delete tag (if mistake)
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# View all tags
git tag -l

# View tag details
git show v1.0.1
```

### URLs

- **GitHub Repository:** `https://github.com/ngroegli/qr-code-utils`
- **Releases:** `https://github.com/ngroegli/qr-code-utils/releases`
- **Actions:** `https://github.com/ngroegli/qr-code-utils/actions`
- **CI Workflow:** `https://github.com/ngroegli/qr-code-utils/actions/workflows/ci.yml`
- **Release Workflow:** `https://github.com/ngroegli/qr-code-utils/actions/workflows/release.yml`

---

## Version History

| Version | Date | Type | Notes |
|---------|------|------|-------|
| v1.0.1 | 2025-01-13 | Patch | Bug fixes and workflow improvements |
| v1.0.0 | 2025-01-13 | Major | Initial stable release |

---

**Need Help?**

- Check the [User Guide](USER_GUIDE.md) for general usage
- See [Testing Guide](TESTING.md) for testing documentation
- Review [Software Architecture](SOFTWARE_ARCHITECTURE.md) for technical details

---

*This release guide is maintained by the QR Code Utils development team.*
