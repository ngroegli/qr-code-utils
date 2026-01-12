"""SMS QR code generator."""

from typing import Optional
from .base import BaseQRGenerator


class SMSQRGenerator(BaseQRGenerator):
    """Generate QR codes for SMS messages."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        phone_number: str,
        message: Optional[str] = None,
        **kwargs
    ) -> str:
        """Prepare SMS data.

        Args:
            phone_number: Recipient phone number
            message: Optional pre-filled message

        Returns:
            SMS formatted string
        """
        # Remove spaces and formatting from phone number
        phone_number = ''.join(filter(str.isdigit, phone_number))

        if message:
            sms_string = f"SMSTO:{phone_number}:{message}"
        else:
            sms_string = f"SMSTO:{phone_number}"

        self.logger.debug("Prepared SMS data for %s", phone_number)
        return sms_string
