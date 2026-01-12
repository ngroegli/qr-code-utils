"""Location/GPS QR code generator."""

from typing import Optional
import urllib.parse
from .base import BaseQRGenerator


class LocationQRGenerator(BaseQRGenerator):
    """Generate QR codes for GPS coordinates."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        latitude: float,
        longitude: float,
        query: Optional[str] = None,
        **kwargs
    ) -> str:
        """Prepare location data.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            query: Optional location name/query

        Returns:
            Geo URI formatted string
        """
        # Use geo URI scheme
        geo_string = f"geo:{latitude},{longitude}"

        if query:
            # Add query parameter for location name
            geo_string += f"?q={latitude},{longitude}({self._url_encode(query)})"

        self.logger.debug("Prepared location data: %s, %s", latitude, longitude)
        return geo_string

    def _url_encode(self, text: str) -> str:
        """URL encode text.

        Args:
            text: Text to encode

        Returns:
            URL encoded text
        """
        return urllib.parse.quote(text)
