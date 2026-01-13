# QR Utils

A comprehensive, modular toolkit for generating various types of QR codes with an easy-to-use command-line interface.

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/ngroegli/qr-code-utils)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

## Features

- **11 QR Code Types**: URL, vCard, WiFi, SMS, Email, Phone, Text, Location, Event, WhatsApp, Payment
- **Logo Embedding**: Add custom logos to QR code centers
- **Configurable**: Centralized configuration with sensible defaults
- **Comprehensive Logging**: Track all operations with detailed logs
- **Easy to Use**: Simple, intuitive CLI interface
- **Modular Architecture**: Clean, extensible codebase
- **Well Documented**: Complete user guide and API reference

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ngroegli/qr-code-utils.git
cd qr-code-utils

# Run the installer (creates venv, installs dependencies, sets up PATH)
chmod +x install.sh
./install.sh

# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

The installer will:
- Create a Python virtual environment
- Install all dependencies
- Set up the `qr-utils` alias in your shell
- Create config directory at `~/.qr-utils`

### Generate Your First QR Code

```bash
# Simple URL QR code
qr-utils url --url "https://example.com"

# WiFi QR code
qr-utils wifi --ssid "MyNetwork" --password "MyPassword"

# vCard contact QR code
qr-utils vcard --first-name "John" --last-name "Doe" --email "john@example.com"
```

## Supported QR Code Types

| Type | Description | Example Use Case |
|------|-------------|------------------|
| **URL** | Website links | Share website URLs |
| **vCard** | Contact information | Digital business cards |
| **WiFi** | Network credentials | Guest WiFi access |
| **SMS** | Pre-filled text messages | Quick contact |
| **Email** | Email with subject/body | Support requests |
| **Phone** | Phone numbers | Click-to-call |
| **Text** | Plain text | Any text content |
| **Location** | GPS coordinates | Share locations |
| **Event** | Calendar events | Event invitations |
| **WhatsApp** | WhatsApp messages | Direct messaging |
| **Payment** | Bitcoin, Ethereum, PayPal | Receive payments |

## Usage Examples

### URL with Logo

```bash
qr-utils url --url "https://example.com" --logo logo.png -o qr_branded.png
```

### WiFi Network

```bash
qr-utils wifi \
  --ssid "CoffeeShop_Guest" \
  --password "Welcome2024" \
  --security WPA \
  -o wifi_qr.png
```

### Business Card (vCard)

```bash
qr-utils vcard \
  --first-name "Jane" \
  --last-name "Smith" \
  --phone "+41763022455" \
  --email "jane@example.com" \
  --organization "Tech Corp" \
  --title "CEO" \
  --logo profile.png \
  -o business_card.png
```

### Calendar Event

```bash
qr-utils event \
  --title "Team Meeting" \
  --start "2026-01-15 14:00" \
  --end "2026-01-15 15:00" \
  --location "Conference Room A" \
  -o event_qr.png
```

### Payment (Bitcoin)

```bash
qr-utils payment \
  --type bitcoin \
  --recipient "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" \
  --amount 0.001 \
  -o bitcoin_qr.png
```

## Project Structure

```
qr-code-utils/
├── qr-utils.sh            # Wrapper script (aliased as qr-utils)
├── install.sh             # Installation script
├── requirements.txt       # Python dependencies
├── venv/                  # Virtual environment (created by installer)
├── src/
│   ├── main.py            # Main CLI entry point
│   ├── common/            # Shared utilities
│   │   ├── config.py      # Configuration management
│   │   └── logger.py      # Logging setup
│   └── core/              # QR generators
│       ├── base.py        # Base generator class
│       ├── url.py         # URL QR generator
│       ├── vcard.py       # vCard generator
│       ├── wifi.py        # WiFi generator
│       ├── sms.py         # SMS generator
│       ├── email.py       # Email generator
│       ├── phone.py       # Phone generator
│       ├── text.py        # Text generator
│       ├── location.py    # Location generator
│       ├── event.py       # Event generator
│       ├── whatsapp.py    # WhatsApp generator
│       └── payment.py     # Payment generator
├── docs/
│   ├── USER_GUIDE.md      # Comprehensive user guide
│   ├── API_REFERENCE.md   # API documentation
│   ├── QUICK_REFERENCE.md # Quick reference guide
│   └── drawings/          # Architecture diagrams (D2 format)
│       ├── architecture.d2
│       ├── flow.d2
│       └── classes.d2
├── install.sh           # Installation script
├── requirements.txt       # Python dependencies
└── README.md             # This file

Configuration & Output (~/.qr-utils/):
├── config.json           # User configuration
├── logs/                 # Application logs
└── output/               # Generated QR codes
```

## Configuration

Configuration is stored in `~/..qr-utils/config.json`:

```json
{
  "qr_settings": {
    "version": 1,
    "error_correction": "H",
    "box_size": 10,
    "border": 4,
    "fill_color": "black",
    "back_color": "white"
  },
  "output_format": "png",
  "default_output_dir": "/home/user/.qr-utils/output"
}
```

### Error Correction Levels

- **L**: ~7% correction
- **M**: ~15% correction
- **Q**: ~25% correction
- **H**: ~30% correction (recommended for logos)

## Documentation

- **[User Guide](docs/USER_GUIDE.md)**: Complete usage guide with examples
- **[API Reference](docs/API_REFERENCE.md)**: Detailed API documentation
- **Architecture Diagrams**: D2 diagrams in `docs/drawings/`
  - `architecture.d2`: System architecture
  - `flow.d2`: Generation flow
  - `classes.d2`: Class hierarchy

## Development

### Installing for Development

```bash
# Clone repository
git clone https://github.com/ngroegli/qr-code-utils.git
cd qr-code-utils

# Run installer to set up venv and dependencies
./install.sh

# Or manually install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running Locally

```bash
# Using the wrapper script (recommended)
./qr-utils url --url "https://example.com"

# Or directly with Python
source venv/bin/activate
python src/main.py url --url "https://example.com"
```

### Creating Custom Generators

Extend `BaseQRGenerator` to create custom QR types:

```python
from src.core.base import BaseQRGenerator

class CustomQRGenerator(BaseQRGenerator):
    def prepare_data(self, custom_param: str, **kwargs) -> str:
        # Format your data
        return f"CUSTOM:{custom_param}"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-qrcode](https://github.com/lincolnloop/python-qrcode) - QR code generation library
- [Pillow](https://python-pillow.org/) - Python Imaging Library

## Architecture

```
┌─────────┐
│  User   │
└────┬────┘
     │ CLI Command
     ▼
┌──────────────────┐
│  src/main.py     │
│  (CLI Handler)   │
└─────┬────────────┘
      │
      │ Initializes & Uses
      ├─────────────┬─────────────┐
      ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌────────────────┐
│ Config   │  │ Logger   │  │ QR Generators  │
│ (Shared) │  │ (Shared) │  ├────────────────┤
└──────────┘  └──────────┘  │ • URL          │
                             │ • vCard        │
                             │ • WiFi         │
                             │ • SMS          │
                             │ • Email        │
                             │ • Phone        │
                             │ • Text         │
                             │ • Location     │
                             │ • Event        │
                             │ • WhatsApp     │
                             │ • Payment      │
                             └────────┬───────┘
                                      ▼
                               ┌─────────────┐
                               │ QR Code PNG │
                               └─────────────┘
```

## Future Enhancements

- [ ] GUI interface
- [ ] Batch QR code generation
- [ ] QR code scanning/reading
- [ ] SVG output format
- [ ] More payment types (Venmo, Cash App, etc.)
- [ ] Custom color schemes
- [ ] QR code templates
- [ ] Web API interface

## Support

If you encounter any issues or have questions:

1. Check the [User Guide](docs/USER_GUIDE.md)
2. Review [API Reference](docs/API_REFERENCE.md)
3. Check logs in `~/..qr-utils/logs/`
4. Open an issue on GitHub

---
