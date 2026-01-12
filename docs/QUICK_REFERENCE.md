# QR Code Utils - Quick Reference

## Installation
```bash
chmod +x install.sh
./install.sh
source ~/.bashrc  # or source ~/.zshrc
```

## Basic Usage
```bash
qr-utils [TYPE] [OPTIONS]
```

All QR codes are saved to `~/.qr-utils/output/` by default with format: `qr_<type>_YYYYMMDD_HHMMSS.png`

## QR Code Types Quick Reference

### 1. URL
```bash
qr-utils url --url "https://example.com"
qr-utils url --url "https://example.com" --logo logo.png -o qr.png
```

### 2. vCard (Contact)
```bash
qr-utils vcard \
  --first-name "John" \
  --last-name "Doe" \
  --phone "+1234567890" \
  --email "john@example.com" \
  --organization "Company" \
  --title "CEO"
```

### 3. WiFi
```bash
qr-utils wifi \
  --ssid "NetworkName" \
  --password "password123" \
  --security WPA
```

### 4. SMS
```bash
qr-utils sms \
  --phone "+1234567890" \
  --message "Hello!"
```

### 5. Email
```bash
qr-utils email \
  --email "contact@example.com" \
  --subject "Subject" \
  --body "Message"
```

### 6. Phone
```bash
qr-utils phone --phone "+1234567890"
```

### 7. Text
```bash
qr-utils text --text "Any text content here"
```

### 8. Location
```bash
qr-utils location \
  --latitude 47.3769 \
  --longitude 8.5417 \
  --query "Zurich"
```

### 9. Event
```bash
qr-utils event \
  --title "Meeting" \
  --start "2026-01-15 14:00" \
  --end "2026-01-15 15:00" \
  --location "Room A"
```

### 10. WhatsApp
```bash
qr-utils whatsapp \
  --phone "1234567890" \
  --message "Hi!"
```

### 11. Payment
```bash
# Bitcoin
qr-utils payment \
  --type bitcoin \
  --recipient "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" \
  --amount 0.001

# PayPal
qr-utils payment \
  --type paypal \
  --recipient "username" \
  --amount 25.00
```

## Common Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output file path |
| `--logo` | `-l` | Logo image path |
| `--config-dir` | | Custom config directory |
| `--help` | `-h` | Show help |

## File Locations

| Purpose | Location |
|---------|----------|
| Configuration | `~/.qr-utils/config.json` |
| Logs | `~/.qr-utils/logs/` |
| Output (default) | `~/.qr-utils/output/` |
| Virtual Environment | `./venv/` |
| Wrapper Script | `./qr-utils.sh` (aliased as `qr-utils`) |

## Error Correction Levels

Edit `~/.qr-utils/config.json`:

```json
{
  "qr_settings": {
    "error_correction": "H"
  }
}
```

- **L**: ~7% correction
- **M**: ~15% correction
- **Q**: ~25% correction
- **H**: ~30% correction (best for logos)

## Customization

### QR Code Appearance
Edit `~/.qr-utils/config.json`:
```json
{
  "qr_settings": {
    "box_size": 10,
    "border": 4,
    "fill_color": "black",
    "back_color": "white"
  }
}
```

### Custom Colors
```json
{
  "qr_settings": {
    "fill_color": "#1a1a1a",
    "back_color": "#ffffff"
  }
}
```

## Troubleshooting

### View Logs
```bash
tail -f ~/.qr-utils/logs/qr-utils_$(date +%Y%m%d).log
```

### Reset Configuration
```bash
rm ~/.qr-utils/config.json
qr-utils url --url "test"  # Recreates config
```

### Check Python Version
```bash
python --version  # Need 3.7+
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt
```

## Tips

1. **Always use `-H` error correction with logos**
2. **Test QR codes before printing**
3. **Keep logos small** (max 1/4 of QR size)
4. **Use absolute paths** for output files
5. **Check logs** for debugging

## Examples Gallery

### Business Card
```bash
qr-utils vcard \
  --first-name "Jane" --last-name "Smith" \
  --phone "+41763022455" \
  --email "jane@example.com" \
  --organization "Tech Corp" --title "Engineer" \
  --url "https://janesmith.dev" \
  --logo profile.png -o business_card.png
```

### Restaurant WiFi
```bash
qr-utils wifi \
  --ssid "Restaurant_Guest" \
  --password "Welcome2024" \
  --logo restaurant_logo.png -o wifi_table.png
```

### Event Invitation
```bash
qr-utils event \
  --title "Annual Gala" \
  --start "2026-03-20 19:00" \
  --end "2026-03-20 23:00" \
  --location "Grand Hotel" \
  --description "Formal attire" \
  --logo company_logo.png -o invitation.png
```

### Product Link
```bash
qr-utils url \
  --url "https://shop.example.com/product/123" \
  --logo brand_logo.png -o product_qr.png
```

## Get Help

```bash
# General help
qr-utils --help

# Type-specific help
qr-utils url --help
qr-utils vcard --help
qr-utils wifi --help
```

## Documentation

- **Full Guide**: `docs/USER_GUIDE.md`
- **API Docs**: `docs/API_REFERENCE.md`
- **Migration**: `MIGRATION_GUIDE.md`
- **Architecture**: `docs/drawings/*.d2`
