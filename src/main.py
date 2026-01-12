#!/usr/bin/env python3
"""
QR Code Utils - Main Entry Point

A comprehensive toolkit for generating various types of QR codes.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from decimal import Decimal

# Add parent directory to path to allow absolute imports from src
sys.path.insert(0, str(Path(__file__).parent.parent))

# pylint: disable=wrong-import-position  # Need to modify path before importing from src
from src.common.config import Config
from src.common.logger import setup_logger
from src.core import (
    URLQRGenerator,
    VCardQRGenerator,
    WiFiQRGenerator,
    SMSQRGenerator,
    EmailQRGenerator,
    PhoneQRGenerator,
    TextQRGenerator,
    LocationQRGenerator,
    EventQRGenerator,
    WhatsAppQRGenerator,
    PaymentQRGenerator,
)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description='QR Code Utils - Generate QR codes for various purposes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate URL QR code
  qr-utils url --url "https://example.com" --output qr_url.png

  # Generate WiFi QR code
  qr-utils wifi --ssid "MyNetwork" --password "MyPassword" --security WPA

  # Generate vCard QR code
  qr-utils vcard --first-name "John" --last-name "Doe" --email "john@example.com"

  # Generate QR code with logo
  qr-utils url --url "https://example.com" --logo logo.png --output qr.png
        """
    )

    parser.add_argument(
        '--config-dir',
        type=str,
        help='Custom configuration directory (default: ~/qr-utils)'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path for QR code'
    )

    parser.add_argument(
        '--logo', '-l',
        type=str,
        help='Logo image to embed in QR code center'
    )

    subparsers = parser.add_subparsers(dest='command', help='QR code type')

    # URL QR Code
    url_parser = subparsers.add_parser('url', help='Generate URL QR code')
    url_parser.add_argument('--url', required=True, help='URL to encode')

    # vCard QR Code
    vcard_parser = subparsers.add_parser('vcard', help='Generate vCard QR code')
    vcard_parser.add_argument('--first-name', required=True, help='First name')
    vcard_parser.add_argument('--last-name', required=True, help='Last name')
    vcard_parser.add_argument('--phone', help='Phone number')
    vcard_parser.add_argument('--email', help='Email address')
    vcard_parser.add_argument('--organization', help='Organization')
    vcard_parser.add_argument('--title', help='Job title')
    vcard_parser.add_argument('--url', help='Website URL')
    vcard_parser.add_argument('--birthday', help='Birthday (YYYYMMDD)')
    vcard_parser.add_argument('--note', help='Additional notes')

    # WiFi QR Code
    wifi_parser = subparsers.add_parser('wifi', help='Generate WiFi QR code')
    wifi_parser.add_argument('--ssid', required=True, help='WiFi SSID')
    wifi_parser.add_argument('--password', required=True, help='WiFi password')
    wifi_parser.add_argument('--security', default='WPA',
                            choices=['WPA', 'WEP', 'nopass'],
                            help='Security type')
    wifi_parser.add_argument('--hidden', action='store_true',
                            help='Network is hidden')

    # SMS QR Code
    sms_parser = subparsers.add_parser('sms', help='Generate SMS QR code')
    sms_parser.add_argument('--phone', required=True, help='Phone number')
    sms_parser.add_argument('--message', help='Pre-filled message')

    # Email QR Code
    email_parser = subparsers.add_parser('email', help='Generate email QR code')
    email_parser.add_argument('--email', required=True, help='Email address')
    email_parser.add_argument('--subject', help='Email subject')
    email_parser.add_argument('--body', help='Email body')

    # Phone QR Code
    phone_parser = subparsers.add_parser('phone', help='Generate phone QR code')
    phone_parser.add_argument('--phone', required=True, help='Phone number')

    # Text QR Code
    text_parser = subparsers.add_parser('text', help='Generate plain text QR code')
    text_parser.add_argument('--text', required=True, help='Text to encode')

    # Location QR Code
    location_parser = subparsers.add_parser('location', help='Generate location QR code')
    location_parser.add_argument('--latitude', type=float, required=True,
                                help='Latitude')
    location_parser.add_argument('--longitude', type=float, required=True,
                                help='Longitude')
    location_parser.add_argument('--query', help='Location name')

    # Event QR Code
    event_parser = subparsers.add_parser('event', help='Generate calendar event QR code')
    event_parser.add_argument('--title', required=True, help='Event title')
    event_parser.add_argument('--start', required=True,
                            help='Start time (YYYY-MM-DD HH:MM)')
    event_parser.add_argument('--end', required=True,
                            help='End time (YYYY-MM-DD HH:MM)')
    event_parser.add_argument('--location', help='Event location')
    event_parser.add_argument('--description', help='Event description')

    # WhatsApp QR Code
    whatsapp_parser = subparsers.add_parser('whatsapp', help='Generate WhatsApp QR code')
    whatsapp_parser.add_argument('--phone', required=True,
                                help='Phone number (with country code)')
    whatsapp_parser.add_argument('--message', help='Pre-filled message')

    # Payment QR Code
    payment_parser = subparsers.add_parser('payment', help='Generate payment QR code')
    payment_parser.add_argument('--type', required=True,
                               choices=['bitcoin', 'ethereum', 'paypal'],
                               help='Payment type')
    payment_parser.add_argument('--recipient', required=True,
                               help='Recipient address/ID')
    payment_parser.add_argument('--amount', type=float, help='Payment amount')
    payment_parser.add_argument('--currency', default='USD', help='Currency code')
    payment_parser.add_argument('--message', help='Payment message')

    return parser


def handle_url(args, config: Config) -> Path:
    """Handle URL QR code generation."""
    generator = URLQRGenerator(config)
    return generator.generate(
        url=args.url,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_vcard(args, config: Config) -> Path:
    """Handle vCard QR code generation."""
    generator = VCardQRGenerator(config)
    return generator.generate(
        first_name=args.first_name,
        last_name=args.last_name,
        phone=args.phone,
        email=args.email,
        organization=args.organization,
        title=args.title,
        url=args.url,
        birthday=args.birthday,
        note=args.note,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_wifi(args, config: Config) -> Path:
    """Handle WiFi QR code generation."""
    generator = WiFiQRGenerator(config)
    return generator.generate(
        ssid=args.ssid,
        password=args.password,
        security=args.security,
        hidden=args.hidden,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_sms(args, config: Config) -> Path:
    """Handle SMS QR code generation."""
    generator = SMSQRGenerator(config)
    return generator.generate(
        phone_number=args.phone,
        message=args.message,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_email(args, config: Config) -> Path:
    """Handle email QR code generation."""
    generator = EmailQRGenerator(config)
    return generator.generate(
        email=args.email,
        subject=args.subject,
        body=args.body,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_phone(args, config: Config) -> Path:
    """Handle phone QR code generation."""
    generator = PhoneQRGenerator(config)
    return generator.generate(
        phone_number=args.phone,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_text(args, config: Config) -> Path:
    """Handle text QR code generation."""
    generator = TextQRGenerator(config)
    return generator.generate(
        text=args.text,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_location(args, config: Config) -> Path:
    """Handle location QR code generation."""
    generator = LocationQRGenerator(config)
    return generator.generate(
        latitude=args.latitude,
        longitude=args.longitude,
        query=args.query,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_event(args, config: Config) -> Path:
    """Handle event QR code generation."""

    generator = EventQRGenerator(config)

    # Parse datetime strings
    start_time = datetime.strptime(args.start, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(args.end, "%Y-%m-%d %H:%M")

    return generator.generate(
        title=args.title,
        start_time=start_time,
        end_time=end_time,
        location=args.location,
        description=args.description,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_whatsapp(args, config: Config) -> Path:
    """Handle WhatsApp QR code generation."""
    generator = WhatsAppQRGenerator(config)
    return generator.generate(
        phone_number=args.phone,
        message=args.message,
        output_path=args.output,
        logo_path=args.logo
    )


def handle_payment(args, config: Config) -> Path:
    """Handle payment QR code generation."""

    generator = PaymentQRGenerator(config)

    amount = Decimal(str(args.amount)) if args.amount else None

    return generator.generate(
        payment_type=args.type,
        recipient=args.recipient,
        amount=amount,
        currency=args.currency,
        message=args.message,
        output_path=args.output,
        logo_path=args.logo
    )


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize configuration
    config_dir = Path(args.config_dir) if args.config_dir else None
    config = Config(config_dir)

    # Setup logger
    logger = setup_logger('main', log_dir=config.logs_dir)

    try:
        # Dispatch to appropriate handler
        handlers = {
            'url': handle_url,
            'vcard': handle_vcard,
            'wifi': handle_wifi,
            'sms': handle_sms,
            'email': handle_email,
            'phone': handle_phone,
            'text': handle_text,
            'location': handle_location,
            'event': handle_event,
            'whatsapp': handle_whatsapp,
            'payment': handle_payment,
        }

        handler = handlers.get(args.command)
        if not handler:
            logger.error("Unknown command: %s", args.command)
            sys.exit(1)

        output_path = handler(args, config)

        print("\n✅ QR code generated successfully!")
        print(f"📁 Output: {output_path}")
        print(f"📋 Config directory: {config.config_dir}")
        print(f"📝 Logs directory: {config.logs_dir}")

    except (ValueError, FileNotFoundError, OSError) as e:
        logger.error("Error: %s", e, exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
