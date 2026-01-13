"""vCard QR code generator."""

from typing import Optional, Dict
from .base import BaseQRGenerator


class VCardQRGenerator(BaseQRGenerator):
    """Generate QR codes for vCard contact information."""

    # pylint: disable=arguments-differ,too-many-arguments
    # Many arguments needed for comprehensive vCard support
    def prepare_data(
        self,
        *,
        first_name: str,
        last_name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        organization: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        address: Optional[Dict[str, str]] = None,
        birthday: Optional[str] = None,
        note: Optional[str] = None,
        version: str = "3.0",
        **kwargs
    ) -> str:
        """Prepare vCard data.

        Args:
            first_name: First name
            last_name: Last name
            phone: Phone number
            email: Email address
            organization: Organization name
            title: Job title
            url: Website URL
            address: Address dictionary with keys: street, city, state, postal_code, country
            birthday: Birthday in YYYYMMDD format
            note: Additional notes
            version: vCard version

        Returns:
            vCard formatted string
        """
        vcard_lines = [
            "BEGIN:VCARD",
            f"VERSION:{version}",
            f"N:{last_name};{first_name}",
            f"FN:{first_name} {last_name}",
        ]

        if organization:
            vcard_lines.append(f"ORG:{organization}")

        if title:
            vcard_lines.append(f"TITLE:{title}")

        if phone:
            vcard_lines.append(f"TEL:{phone}")

        if email:
            vcard_lines.append(f"EMAIL:{email}")

        if url:
            vcard_lines.append(f"URL:{url}")

        if address:
            # Format: ;;street;city;state;postal_code;country
            # pylint: disable=unnecessary-semicolon  # Semicolons are part of vCard format, not Python syntax
            addr_str = f";;{address.get('street', '')};{address.get('city', '')};" \
                      f"{address.get('state', '')};{address.get('postal_code', '')};" \
                      f"{address.get('country', '')}"
            vcard_lines.append(f"ADR;TYPE=work:{addr_str}")

        if birthday:
            vcard_lines.append(f"BDAY:{birthday}")

        if note:
            vcard_lines.append(f"NOTE:{note}")

        vcard_lines.append("END:VCARD")

        vcard_data = "\n".join(vcard_lines)
        self.logger.debug("Prepared vCard data")
        return vcard_data
