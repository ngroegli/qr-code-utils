"""WhatsApp QR code generator."""

from typing import Optional
from .base import BaseQRGenerator
import urllib.parse


class WhatsAppQRGenerator(BaseQRGenerator):
    """Generate QR codes for WhatsApp messages."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        phone_number: str,
        message: Optional[str] = None,
        **kwargs
    ) -> str:
        """Prepare WhatsApp data.

        Args:
            phone_number: Recipient phone number (with country code, no +)
            message: Optional pre-filled message

        Returns:
            WhatsApp URL formatted string
        """
        # Remove all non-digit characters except ensure it starts without +
        phone_number = ''.join(filter(str.isdigit, phone_number))

        whatsapp_url = f"https://wa.me/{phone_number}"

        if message:
            encoded_message = self._url_encode(message)
            whatsapp_url += f"?text={encoded_message}"

        self.logger.debug("Prepared WhatsApp data for %s", phone_number)
        return whatsapp_url

    def _url_encode(self, text: str) -> str:
        """URL encode text.

        Args:
            text: Text to encode

        Returns:
            URL encoded text
        """
        return urllib.parse.quote(text)
