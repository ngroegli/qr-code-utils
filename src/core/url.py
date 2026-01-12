"""URL QR code generator."""

from .base import BaseQRGenerator


class URLQRGenerator(BaseQRGenerator):
    """Generate QR codes for URLs."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(self, *, url: str, **kwargs) -> str:
        """Prepare URL data.

        Args:
            url: URL to encode

        Returns:
            URL string
        """
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        self.logger.debug("Prepared URL: %s", url)
        return url
