"""WiFi QR code generator."""

from .base import BaseQRGenerator


class WiFiQRGenerator(BaseQRGenerator):
    """Generate QR codes for WiFi credentials."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        ssid: str,
        password: str,
        security: str = "WPA",
        hidden: bool = False,
        **kwargs
    ) -> str:
        """Prepare WiFi data.

        Args:
            ssid: Network SSID
            password: Network password
            security: Security type (WPA, WEP, or nopass)
            hidden: Whether network is hidden

        Returns:
            WiFi formatted string
        """
        # Escape special characters
        ssid = self._escape_special_chars(ssid)
        password = self._escape_special_chars(password)

        hidden_flag = "true" if hidden else "false"

        wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden_flag};;"

        self.logger.debug("Prepared WiFi data for SSID: %s", ssid)
        return wifi_string

    def _escape_special_chars(self, text: str) -> str:
        """Escape special characters for WiFi QR format.

        Args:
            text: Text to escape

        Returns:
            Escaped text
        """
        special_chars = ['\\', ';', ',', ':', '"']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
