# QR Code Utils - API Reference

## Overview

This document provides detailed API documentation for QR Code Utils. The project uses a modular architecture with clear separation between common utilities and QR generator implementations.

## Module Structure

```
qr-code-utils/
├── qr-utils.sh              # Wrapper script
├── install.sh               # Automated installer
└── src/
    ├── main.py              # CLI entry point
    ├── common/              # Shared utilities
    │   ├── config.py        # Configuration management
    │   └── logger.py        # Logging setup
    └── core/                # QR generator implementations
        ├── base.py          # Abstract base class
        ├── url.py           # URL QR codes
        ├── vcard.py         # vCard contact QR codes
        ├── wifi.py          # WiFi credential QR codes
        ├── sms.py           # SMS message QR codes
        ├── email.py         # Email mailto QR codes
        ├── phone.py         # Phone number QR codes
        ├── text.py          # Plain text QR codes
        ├── location.py      # GPS location QR codes
        ├── event.py         # Calendar event QR codes
        ├── whatsapp.py      # WhatsApp message QR codes
        └── payment.py       # Payment QR codes

User Configuration:
~/.qr-utils/
├── config.json              # User configuration
├── logs/                    # Application logs
└── output/                  # Default QR code output directory
```

## Common Module

### Config Class

**Location:** `src/common/config.py`

Configuration manager for QR Code Utils.

#### Constructor

```python
Config(config_dir: Optional[Path] = None)
```

**Parameters:**
- `config_dir`: Optional custom configuration directory (default: `~/.qr-utils`)

#### Methods

##### `get(key: str, default: Any = None) -> Any`

Get configuration value with dot notation support.

```python
config = Config()
box_size = config.get('qr_settings.box_size', 10)
```

##### `set(key: str, value: Any, save: bool = True)`

Set configuration value.

```python
config.set('qr_settings.box_size', 15)
```

##### `get_qr_settings() -> Dict[str, Any]`

Get QR code settings dictionary.

##### `get_output_path(filename: str) -> Path`

Get full output path for a file.

### Logger Setup

**Location:** `src/common/logger.py`

#### Function

```python
setup_logger(
    name: str,
    log_dir: Optional[Path] = None,
    level: int = logging.INFO,
    console: bool = True
) -> logging.Logger
```

**Parameters:**
- `name`: Logger name
- `log_dir`: Directory for log files
- `level`: Logging level (default: INFO)
- `console`: Enable console output (default: True)

**Returns:** Configured Logger instance

## Core Module

### BaseQRGenerator (Abstract)

**Location:** `src/core/base.py`

Abstract base class for all QR code generators.

#### Constructor

```python
BaseQRGenerator(config: Optional[Config] = None)
```

#### Abstract Methods

##### `prepare_data(**kwargs) -> str`

Must be implemented by subclasses to format data for QR encoding.

#### Public Methods

##### `create_qr_code(data: str, custom_settings: Optional[Dict] = None) -> Image.Image`

Create a QR code PIL Image from data.

**Parameters:**
- `data`: String data to encode
- `custom_settings`: Optional settings override

**Returns:** PIL Image object

##### `add_logo(qr_image: Image.Image, logo_path: str, logo_size: Optional[tuple] = None) -> Image.Image`

Add logo to QR code center.

**Parameters:**
- `qr_image`: QR code image
- `logo_path`: Path to logo file
- `logo_size`: Optional custom logo size (width, height)

**Returns:** QR code image with logo

##### `generate(output_path: Optional[str] = None, logo_path: Optional[str] = None, custom_settings: Optional[Dict] = None, **kwargs) -> Path`

Main method to generate and save QR code.

**Parameters:**
- `output_path`: Output file path
- `logo_path`: Optional logo path
- `custom_settings`: Optional QR settings
- `**kwargs`: Passed to `prepare_data()`

**Returns:** Path to saved QR code

### URLQRGenerator

**Location:** `src/core/url.py`

Generate QR codes for URLs.

#### Usage

```python
from src.core import URLQRGenerator

generator = URLQRGenerator()
output_path = generator.generate(
    url="https://example.com",
    output_path="qr_url.png",
    logo_path="logo.png"
)
```

#### Methods

##### `prepare_data(url: str, **kwargs) -> str`

**Parameters:**
- `url`: URL to encode (automatically adds https:// if missing)

### VCardQRGenerator

**Location:** `src/core/vcard.py`

Generate QR codes for vCard contact information.

#### Usage

```python
from src.core import VCardQRGenerator

generator = VCardQRGenerator()
output_path = generator.generate(
    first_name="John",
    last_name="Doe",
    phone="+1234567890",
    email="john@example.com",
    organization="Acme Corp",
    title="CEO",
    url="https://johndoe.com",
    birthday="19900115",
    note="Contact me anytime",
    output_path="qr_vcard.png"
)
```

#### Methods

##### `prepare_data(...) -> str`

**Parameters:**
- `first_name`: First name (required)
- `last_name`: Last name (required)
- `phone`: Phone number
- `email`: Email address
- `organization`: Organization name
- `title`: Job title
- `url`: Website URL
- `address`: Dictionary with street, city, state, postal_code, country
- `birthday`: Birthday (YYYYMMDD)
- `note`: Additional notes
- `version`: vCard version (default: "3.0")

### WiFiQRGenerator

**Location:** `src/core/wifi.py`

Generate QR codes for WiFi credentials.

#### Usage

```python
from src.core import WiFiQRGenerator

generator = WiFiQRGenerator()
output_path = generator.generate(
    ssid="MyNetwork",
    password="SecurePassword",
    security="WPA",
    hidden=False,
    output_path="qr_wifi.png"
)
```

#### Methods

##### `prepare_data(ssid: str, password: str, security: str = "WPA", hidden: bool = False, **kwargs) -> str`

**Parameters:**
- `ssid`: Network SSID (required)
- `password`: Network password (required)
- `security`: "WPA", "WEP", or "nopass" (default: "WPA")
- `hidden`: Network is hidden (default: False)

### SMSQRGenerator

**Location:** `src/core/sms.py`

Generate QR codes for SMS messages.

#### Usage

```python
from src.core import SMSQRGenerator

generator = SMSQRGenerator()
output_path = generator.generate(
    phone_number="+1234567890",
    message="Hello from QR!",
    output_path="qr_sms.png"
)
```

#### Methods

##### `prepare_data(phone_number: str, message: Optional[str] = None, **kwargs) -> str`

### EmailQRGenerator

**Location:** `src/core/email.py`

Generate QR codes for email messages.

#### Usage

```python
from src.core import EmailQRGenerator

generator = EmailQRGenerator()
output_path = generator.generate(
    email="contact@example.com",
    subject="Inquiry",
    body="I would like to know more...",
    output_path="qr_email.png"
)
```

#### Methods

##### `prepare_data(email: str, subject: Optional[str] = None, body: Optional[str] = None, **kwargs) -> str`

### PhoneQRGenerator

**Location:** `src/core/phone.py`

Generate QR codes for phone numbers.

#### Usage

```python
from src.core import PhoneQRGenerator

generator = PhoneQRGenerator()
output_path = generator.generate(
    phone_number="+1234567890",
    output_path="qr_phone.png"
)
```

### TextQRGenerator

**Location:** `src/core/text.py`

Generate QR codes for plain text.

#### Usage

```python
from src.core import TextQRGenerator

generator = TextQRGenerator()
output_path = generator.generate(
    text="Hello, World!",
    output_path="qr_text.png"
)
```

### LocationQRGenerator

**Location:** `src/core/location.py`

Generate QR codes for geographic locations.

#### Usage

```python
from src.core import LocationQRGenerator

generator = LocationQRGenerator()
output_path = generator.generate(
    latitude=47.3769,
    longitude=8.5417,
    query="Zurich, Switzerland",
    output_path="qr_location.png"
)
```

#### Methods

##### `prepare_data(latitude: float, longitude: float, query: Optional[str] = None, **kwargs) -> str`

### EventQRGenerator

**Location:** `src/core/event.py`

Generate QR codes for calendar events.

#### Usage

```python
from src.core import EventQRGenerator
from datetime import datetime

generator = EventQRGenerator()
output_path = generator.generate(
    title="Team Meeting",
    start_time=datetime(2026, 1, 15, 14, 0),
    end_time=datetime(2026, 1, 15, 15, 0),
    location="Conference Room A",
    description="Monthly sync",
    output_path="qr_event.png"
)
```

#### Methods

##### `prepare_data(title: str, start_time: datetime, end_time: datetime, location: Optional[str] = None, description: Optional[str] = None, **kwargs) -> str`

### WhatsAppQRGenerator

**Location:** `src/core/whatsapp.py`

Generate QR codes for WhatsApp messages.

#### Usage

```python
from src.core import WhatsAppQRGenerator

generator = WhatsAppQRGenerator()
output_path = generator.generate(
    phone_number="1234567890",
    message="Hi! I scanned your QR code.",
    output_path="qr_whatsapp.png"
)
```

#### Methods

##### `prepare_data(phone_number: str, message: Optional[str] = None, **kwargs) -> str`

### PaymentQRGenerator

**Location:** `src/core/payment.py`

Generate QR codes for payment information.

#### Usage

```python
from src.core import PaymentQRGenerator
from decimal import Decimal

generator = PaymentQRGenerator()

# Bitcoin
output_path = generator.generate(
    payment_type="bitcoin",
    recipient="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    amount=Decimal("0.001"),
    message="Donation",
    output_path="qr_bitcoin.png"
)

# PayPal
output_path = generator.generate(
    payment_type="paypal",
    recipient="username",
    amount=Decimal("25.00"),
    currency="USD",
    output_path="qr_paypal.png"
)
```

#### Methods

##### `prepare_data(payment_type: str, recipient: str, amount: Optional[Decimal] = None, currency: Optional[str] = None, message: Optional[str] = None, **kwargs) -> str`

**Parameters:**
- `payment_type`: "bitcoin", "ethereum", or "paypal"
- `recipient`: Address or username
- `amount`: Payment amount
- `currency`: Currency code (for PayPal)
- `message`: Payment note

## Custom Settings

All generators support custom QR settings via the `custom_settings` parameter:

```python
custom_settings = {
    "version": 1,
    "error_correction": "H",  # L, M, Q, H
    "box_size": 10,
    "border": 4,
    "fill_color": "black",
    "back_color": "white"
}

generator.generate(..., custom_settings=custom_settings)
```

## Error Handling

All generators raise exceptions on errors. Wrap calls in try-except:

```python
try:
    output_path = generator.generate(...)
except Exception as e:
    logger.error(f"Failed to generate QR code: {e}")
```

## Example: Custom Integration

```python
from pathlib import Path
from src.common import Config, setup_logger
from src.core import URLQRGenerator

# Setup
config = Config(Path.home() / "my-qr-app")
logger = setup_logger("my-app", log_dir=config.logs_dir)

# Generate
generator = URLQRGenerator(config)
try:
    output = generator.generate(
        url="https://example.com",
        logo_path="logo.png"
    )
    logger.info(f"QR code generated: {output}")
except Exception as e:
    logger.error(f"Error: {e}")
```
