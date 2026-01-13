# Software Architecture

**QR Code Utils v1.0**
**Last Updated:** January 13, 2025

This document describes the software architecture, design patterns, and technical implementation details.

## Architecture Overview

![System Architecture](drawings/architecture.png)

QR Code Utils follows a **modular, object-oriented architecture** with clear separation of concerns.

## System Components

### 1. CLI Interface
- **qr-utils.sh**: Shell wrapper
- **main.py**: Entry point with argparse

### 2. Common Modules
- **Config**: Settings management
- **Logger**: Structured logging

### 3. QR Generator Core
- **BaseQRGenerator**: Abstract base class
- **11 Generators**: URL, vCard, WiFi, SMS, Email, Phone, Text, Location, Event, WhatsApp, Payment

### 4. File System
- **~/.qr-utils/**: Configuration directory
  - config.yml
  - logs/
  - output/

### 5. External Libraries
- **qrcode**: QR generation
- **Pillow**: Image processing

## Design Patterns

### 1. Template Method Pattern
BaseQRGenerator defines the algorithm, subclasses implement `prepare_data()`.

### 2. Strategy Pattern
Each generator is a strategy for a specific QR type.

### 3. Factory Pattern
main.py creates appropriate generators based on user input.

### 4. Dependency Injection
Config and logger injected into generators.

## Class Hierarchy

![Class Hierarchy](drawings/classes.png)

All 11 generators inherit from BaseQRGenerator:
- URLQRGenerator
- VCardQRGenerator
- WiFiQRGenerator
- SMSQRGenerator
- EmailQRGenerator
- PhoneQRGenerator
- TextQRGenerator
- LocationQRGenerator
- EventQRGenerator
- WhatsAppQRGenerator
- PaymentQRGenerator

## Execution Flow

![Execution Flow](drawings/flow.png)

1. User invokes qr-utils.sh
2. Parse CLI arguments
3. Initialize config and logger
4. Select appropriate generator
5. Prepare data (generator-specific)
6. Create QR code with qrcode library
7. Optional logo overlay with PIL
8. Save to ~/.qr-utils/output/
9. Return file path

## Extension Points

### Adding a New Generator

1. Create file in src/core/
2. Inherit from BaseQRGenerator
3. Implement prepare_data()
4. Export in __init__.py
5. Add CLI arguments in main.py
6. Write tests

Example:
```python
from .base import BaseQRGenerator

class MyNewQRGenerator(BaseQRGenerator):
    def prepare_data(self, **kwargs) -> str:
        return formatted_data
```

## Technical Specifications

- **Python**: 3.12 (minimum 3.8)
- **Code Quality**: 10.00/10 pylint score
- **Tests**: 67 unit + 5 integration
- **Platform**: Linux, macOS, Windows

## Performance

- QR generation: 50-200ms
- With logo: +50-100ms
- Memory: ~20MB base, +5-10MB per generation

## Security

- Input validation and sanitization
- Safe file path handling
- Regular dependency scanning
- CodeQL static analysis

For more details, see the [Release Guide](RELEASE_GUIDE.md) and [User Guide](USER_GUIDE.md).

---

**Version:** 1.0
**Last Updated:** January 13, 2025
