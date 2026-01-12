"""Email QR code generator."""

import urllib.parse
from typing import Optional
from .base import BaseQRGenerator


class EmailQRGenerator(BaseQRGenerator):
    """Generate QR codes for email addresses with optional subject and body."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        email: str,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        **kwargs
    ) -> str:
        """Prepare email data.

        Args:
            email: Recipient email address
            subject: Optional email subject
            body: Optional email body

        Returns:
            Mailto formatted string
        """
        mailto_string = f"mailto:{email}"

        params = []
        if subject:
            params.append(f"subject={self._url_encode(subject)}")
        if body:
            params.append(f"body={self._url_encode(body)}")

        if params:
            mailto_string += "?" + "&".join(params)

        self.logger.debug("Prepared email data for %s", email)
        return mailto_string

    def _url_encode(self, text: str) -> str:
        """URL encode text.

        Args:
            text: Text to encode

        Returns:
            URL encoded text
        """
        return urllib.parse.quote(text)
