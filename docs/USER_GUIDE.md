# QR Code Utils - User Guide

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [QR Code Types](#qr-code-types)
- [Advanced Features](#advanced-features)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Introduction

QR Code Utils is a comprehensive, production-ready toolkit for generating various types of QR codes. It supports 11 different QR code types with a unified, easy-to-use command-line interface.

### Features
- **11 QR Code Types**: URL, vCard, WiFi, SMS, Email, Phone, Text, Location, Event, WhatsApp, and Payment
- **Logo Embedding**: Add custom logos to QR code centers
- **Virtual Environment**: Isolated Python environment for clean dependency management
- **System-Wide Access**: Shell alias for convenient access from anywhere
- **Configurable**: JSON-based configuration with sensible defaults
- **Comprehensive Logging**: Detailed logs for debugging and tracking
- **User-Friendly**: Simple CLI interface with helpful error messages

## Installation

### Automated Installation (Recommended)

Run the installer script:

```bash
cd qr-code-utils
chmod +x install.sh
./install.sh
```

The installer will:
1. Create a Python virtual environment in `venv/`
2. Install all required dependencies
3. Create `~/.qr-utils/` directory for config, logs, and output
4. Set up the `qr-utils` shell alias in `.bashrc` and/or `.zshrc`

After installation, reload your shell configuration:

```bash
source ~/.bashrc  # for bash
# or
source ~/.zshrc   # for zsh
```

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create config directory
mkdir -p ~/.qr-utils/{logs,output}

# Use the wrapper script
./qr-utils.sh url --url "https://example.com"
```

## Quick Start

Generate your first QR code:

```bash
# Simple URL QR code
qr-utils url --url "https://example.com"

# WiFi QR code
qr-utils wifi --ssid "MyNetwork" --password "MyPassword"

# vCard contact QR code
qr-utils vcard --first-name "John" --last-name "Doe" --email "john@example.com"
```

## Usage Guide

### Basic Command Structure

```bash
qr-utils [TYPE] [OPTIONS] --output [OUTPUT_FILE]
```

### Common Options

- `--output`, `-o`: Specify output file path
- `--logo`, `-l`: Add a logo to the QR code center
- `--config-dir`: Use custom configuration directory (default: `~/.qr-utils`)

## QR Code Types

### 1. URL QR Code

Generate QR codes for websites:

```bash
qr-utils url --url "https://example.com" -o qr_url.png
```

**Parameters:**
- `--url`: URL to encode (required)

### 2. vCard QR Code

Create contact information QR codes:

```bash
qr-utils vcard \
  --first-name "John" \
  --last-name "Doe" \
  --phone "+1234567890" \
  --email "john@example.com" \
  --organization "Acme Corp" \
  --title "CEO" \
  --url "https://johndoe.com" \
  -o qr_vcard.png
```

**Parameters:**
- `--first-name`: First name (required)
- `--last-name`: Last name (required)
- `--phone`: Phone number
- `--email`: Email address
- `--organization`: Organization name
- `--title`: Job title
- `--url`: Website URL
- `--birthday`: Birthday (YYYYMMDD format)
- `--note`: Additional notes

### 3. WiFi QR Code

Share WiFi credentials:

```bash
qr-utils wifi \
  --ssid "MyNetwork" \
  --password "SecurePassword123" \
  --security WPA \
  -o qr_wifi.png
```

**Parameters:**
- `--ssid`: WiFi network name (required)
- `--password`: WiFi password (required)
- `--security`: Security type - WPA, WEP, or nopass (default: WPA)
- `--hidden`: Flag for hidden networks

### 4. SMS QR Code

Pre-fill SMS messages:

```bash
qr-utils sms \
  --phone "+1234567890" \
  --message "Hello from QR code!" \
  -o qr_sms.png
```

**Parameters:**
- `--phone`: Recipient phone number (required)
- `--message`: Pre-filled message text

### 5. Email QR Code

Create email QR codes:

```bash
qr-utils email \
  --email "contact@example.com" \
  --subject "Inquiry" \
  --body "I would like to know more about..." \
  -o qr_email.png
```

**Parameters:**
- `--email`: Recipient email address (required)
- `--subject`: Email subject
- `--body`: Email body text

### 6. Phone QR Code

Dial phone numbers:

```bash
qr-utils phone --phone "+1234567890" -o qr_phone.png
```

**Parameters:**
- `--phone`: Phone number to dial (required)

### 7. Text QR Code

Encode plain text:

```bash
qr-utils text --text "Hello, World!" -o qr_text.png
```

**Parameters:**
- `--text`: Text to encode (required)

### 8. Location QR Code

Share geographic locations:

```bash
qr-utils location \
  --latitude 47.3769 \
  --longitude 8.5417 \
  --query "Zurich, Switzerland" \
  -o qr_location.png
```

**Parameters:**
- `--latitude`: Latitude coordinate (required)
- `--longitude`: Longitude coordinate (required)
- `--query`: Location name/description

### 9. Event QR Code

Create calendar event QR codes:

```bash
qr-utils event \
  --title "Team Meeting" \
  --start "2026-01-15 14:00" \
  --end "2026-01-15 15:00" \
  --location "Conference Room A" \
  --description "Monthly team sync" \
  -o qr_event.png
```

**Parameters:**
- `--title`: Event title (required)
- `--start`: Start time in "YYYY-MM-DD HH:MM" format (required)
- `--end`: End time in "YYYY-MM-DD HH:MM" format (required)
- `--location`: Event location
- `--description`: Event description

### 10. WhatsApp QR Code

Open WhatsApp chats:

```bash
qr-utils whatsapp \
  --phone "1234567890" \
  --message "Hi! I scanned your QR code." \
  -o qr_whatsapp.png
```

**Parameters:**
- `--phone`: Phone number with country code, without + (required)
- `--message`: Pre-filled message

### 11. Payment QR Code

Generate payment QR codes:

```bash
# Bitcoin
qr-utils payment \
  --type bitcoin \
  --recipient "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" \
  --amount 0.001 \
  --message "Donation" \
  -o qr_bitcoin.png

# PayPal
qr-utils payment \
  --type paypal \
  --recipient "your-paypal-username" \
  --amount 25.00 \
  --currency USD \
  -o qr_paypal.png
```

**Parameters:**
- `--type`: Payment type - bitcoin, ethereum, or paypal (required)
- `--recipient`: Recipient address/ID (required)
- `--amount`: Payment amount
- `--currency`: Currency code (for PayPal, default: USD)
- `--message`: Payment message/note

## Advanced Features

### Adding Logos

Add a custom logo to any QR code:

```bash
qr-utils url --url "https://example.com" --logo logo.png -o qr_with_logo.png
```

**Logo Requirements:**
- Supported formats: PNG, JPG, JPEG
- Recommended: Square images with transparent background (PNG)
- The logo will be automatically resized to 1/4 of the QR code size

### Custom Output Directory

Specify a custom output location:

```bash
qr-utils url --url "https://example.com" -o /path/to/custom/location/qr.png
```

### Custom Configuration Directory

Use a different configuration directory:

```bash
qr-utils url --url "https://example.com" --config-dir /path/to/config
```

## Configuration

Configuration is stored in `~/.qr-utils/config.yml`:

```yaml
qr_settings:
  version: 1
  error_correction: H  # L, M, Q, or H
  box_size: 10
  border: 4
  fill_color: black
  back_color: white

output_format: png
default_output_dir: /home/user/.qr-utils/output
```

### QR Settings

- **version**: QR code version (1-40, where 1 is 21x21 and 40 is 177x177)
- **error_correction**: Error correction level
  - `L`: ~7% correction
  - `M`: ~15% correction
  - `Q`: ~25% correction
  - `H`: ~30% correction (recommended for logos)
- **box_size**: Size of each box in pixels
- **border**: Border size in boxes
- **fill_color**: QR code foreground color
- **back_color**: QR code background color

## Examples

### Personal Business Card

```bash
qr-utils vcard \
  --first-name "Jane" \
  --last-name "Smith" \
  --phone "+41763022455" \
  --email "jane.smith@example.com" \
  --organization "Tech Innovations AG" \
  --title "Software Engineer" \
  --url "https://janesmith.dev" \
  --logo profile_pic.png \
  -o business_card_qr.png
```

### Restaurant WiFi

```bash
qr-utils wifi \
  --ssid "Restaurant_Guest" \
  --password "Welcome2024" \
  --security WPA \
  --logo restaurant_logo.png \
  -o wifi_table_card.png
```

### Event Invitation

```bash
qr-utils event \
  --title "Annual Company Gala" \
  --start "2026-03-20 19:00" \
  --end "2026-03-20 23:00" \
  --location "Grand Hotel Ballroom" \
  --description "Formal attire required. Dinner and entertainment provided." \
  --logo company_logo.png \
  -o event_invitation_qr.png
```

### Product Link with Tracking

```bash
qr-utils url \
  --url "https://shop.example.com/products/item123?ref=qr_packaging" \
  --logo brand_logo.png \
  -o product_qr.png
```

## Troubleshooting

### Common Issues

**1. Module not found errors**
```bash
pip install -r requirements.txt
```

**2. Permission denied**
```bash
chmod +x install.sh
chmod +x main.py
```

**3. QR code not scanning**
- Increase error correction level to 'H'
- Reduce logo size
- Ensure good contrast between foreground and background
- Test with multiple QR code scanners

**4. Logo not appearing**
- Verify logo file exists and path is correct
- Try PNG format with transparent background
- Check logo file permissions

**5. Configuration not loading**
```bash
# Reset configuration
rm -rf ~/.qr-utils/config.yml
qr-utils url --url "https://example.com"
```

### Getting Help

Check logs in `~/.qr-utils/logs/` for detailed error information:

```bash
tail -f ~/.qr-utils/logs/qr-utils_$(date +%Y%m%d).log
```

## Directory Structure

```
~/.qr-utils/
├── config.yml         # Configuration file
├── logs/              # Log files
│   └── qr-utils_YYYYMMDD.log
└── output/            # Generated QR codes (if no output path specified)
    └── *.png
```

## Tips & Best Practices

1. **Use High Error Correction**: When adding logos, use `-H` error correction
2. **Test Before Printing**: Always test QR codes with multiple scanner apps
3. **Size Matters**: For printed QR codes, ensure minimum 2x2 cm size
4. **Color Contrast**: Maintain high contrast for better scanning
5. **Logo Size**: Keep logos to max 1/4 of QR code size
6. **Data Limits**: Keep data concise; longer data = more complex QR code
7. **Version Control**: Keep track of which QR codes are used where

## License

See LICENSE file for details.
