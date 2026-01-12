"""Phone QR code generator."""

from .base import BaseQRGenerator


class PhoneQRGenerator(BaseQRGenerator):
    """Generate QR codes for phone numbers."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        phone_number: str,
        **kwargs
    ) -> str:
        """Prepare phone data.

        Args:
            phone_number: Phone number to call

        Returns:
            Tel formatted string
        """
        # Remove spaces and formatting, keep + for international
        phone_number = ''.join(c for c in phone_number if c.isdigit() or c == '+')

        tel_string = f"tel:{phone_number}"

        self.logger.debug("Prepared phone data for %s", phone_number)
        return tel_string
