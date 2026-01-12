"""Payment QR code generator."""

from typing import Optional
from decimal import Decimal
from .base import BaseQRGenerator
import urllib.parse


class PaymentQRGenerator(BaseQRGenerator):
    """Generate QR codes for payment information."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        payment_type: str,
        recipient: str,
        amount: Optional[Decimal] = None,
        currency: Optional[str] = None,
        message: Optional[str] = None,
        **kwargs
    ) -> str:
        """Prepare payment data.

        Args:
            payment_type: Payment type (bitcoin, ethereum, paypal, etc.)
            recipient: Recipient address/ID
            amount: Payment amount
            currency: Currency code (for PayPal)
            message: Payment message/note

        Returns:
            Payment formatted string
        """
        payment_type = payment_type.lower()

        if payment_type == "bitcoin":
            return self._prepare_bitcoin(recipient, amount, message)
        elif payment_type == "ethereum":
            return self._prepare_ethereum(recipient, amount, message)
        elif payment_type == "paypal":
            return self._prepare_paypal(recipient, amount, currency, message)
        else:
            # Generic format
            payment_string = f"{payment_type}:{recipient}"
            if amount:
                payment_string += f"?amount={amount}"
            if message:
                payment_string += f"&message={self._url_encode(message)}"
            return payment_string

    def _prepare_bitcoin(
        self,
        address: str,
        amount: Optional[Decimal] = None,
        message: Optional[str] = None
    ) -> str:
        """Prepare Bitcoin payment data."""
        btc_string = f"bitcoin:{address}"

        params = []
        if amount:
            params.append(f"amount={amount}")
        if message:
            params.append(f"message={self._url_encode(message)}")

        if params:
            btc_string += "?" + "&".join(params)

        self.logger.debug("Prepared Bitcoin payment data")
        return btc_string

    def _prepare_ethereum(
        self,
        address: str,
        amount: Optional[Decimal] = None,
        message: Optional[str] = None
    ) -> str:
        """Prepare Ethereum payment data."""
        eth_string = f"ethereum:{address}"

        params = []
        if amount:
            params.append(f"value={amount}")
        if message:
            params.append(f"message={self._url_encode(message)}")

        if params:
            eth_string += "?" + "&".join(params)

        self.logger.debug("Prepared Ethereum payment data")
        return eth_string

    def _prepare_paypal(
        self,
        email: str,
        amount: Optional[Decimal] = None,
        currency: Optional[str] = "USD",
        message: Optional[str] = None  # pylint: disable=unused-argument
    ) -> str:
        """Prepare PayPal payment data."""
        paypal_url = f"https://www.paypal.com/paypalme/{email}"

        if amount:
            paypal_url += f"/{amount}{currency}"

        self.logger.debug("Prepared PayPal payment data")
        return paypal_url

    def _url_encode(self, text: str) -> str:
        """URL encode text."""
        return urllib.parse.quote(text)
