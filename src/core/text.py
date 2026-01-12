"""Plain text QR code generator."""

from .base import BaseQRGenerator


class TextQRGenerator(BaseQRGenerator):
    """Generate QR codes for plain text."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        text: str,
        **kwargs
    ) -> str:
        """Prepare text data.

        Args:
            text: Text to encode

        Returns:
            Text string
        """
        self.logger.debug("Prepared text data: %s...", text[:50])
        return text
