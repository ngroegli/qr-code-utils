"""Base QR code generator."""

from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import qrcode
import qrcode.constants
from PIL import Image

from ..common.config import Config
from ..common.logger import setup_logger


class BaseQRGenerator(ABC):
    """Base class for all QR code generators."""

    ERROR_CORRECTION_MAP = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H,
    }

    def __init__(self, config: Optional[Config] = None):
        """Initialize the QR generator.

        Args:
            config: Configuration object
        """
        self.config = config or Config()
        self.logger = setup_logger(
            self.__class__.__name__,
            log_dir=self.config.logs_dir
        )
        self.qr_settings = self.config.get_qr_settings()

    @abstractmethod
    def prepare_data(self, **kwargs) -> str:
        """Prepare data to be encoded in the QR code.

        Args:
            **kwargs: Keyword arguments specific to QR type (e.g., url, email, phone_number, etc.)

        Returns:
            String data to encode
        """
        raise NotImplementedError("Subclasses must implement prepare_data")

    def create_qr_code(
        self,
        data: str,
        custom_settings: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Create a QR code image.

        Args:
            data: Data to encode
            custom_settings: Optional custom QR settings

        Returns:
            PIL Image object
        """
        settings = self.qr_settings.copy()
        if custom_settings:
            settings.update(custom_settings)

        error_correction = self.ERROR_CORRECTION_MAP.get(
            settings.get('error_correction', 'H'),
            qrcode.constants.ERROR_CORRECT_H
        )

        qr = qrcode.QRCode(
            version=settings.get('version', 1),
            error_correction=error_correction,
            box_size=settings.get('box_size', 10),
            border=settings.get('border', 4),
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=settings.get('fill_color', 'black'),
            back_color=settings.get('back_color', 'white')
        )

        return img

    def add_logo(
        self,
        qr_image: Image.Image,
        logo_path: str,
        logo_size: Optional[tuple] = None
    ) -> Image.Image:
        """Add a logo to the center of the QR code.

        Args:
            qr_image: QR code image
            logo_path: Path to logo image
            logo_size: Size to resize logo to (width, height)

        Returns:
            QR code image with logo
        """
        logo = Image.open(logo_path)

        # Calculate logo size if not provided
        if not logo_size:
            qr_width, qr_height = qr_image.size
            logo_size = (qr_width // 4, qr_height // 4)

        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

        # Calculate position to paste logo at center
        pos = (
            (qr_image.size[0] - logo.size[0]) // 2,
            (qr_image.size[1] - logo.size[1]) // 2
        )

        # Convert QR image to RGB if necessary
        if qr_image.mode != 'RGB':
            qr_image = qr_image.convert('RGB')

        # Ensure logo has proper mode for pasting
        if logo.mode == 'RGBA':
            qr_image.paste(logo, pos, logo)
        else:
            if logo.mode != 'RGB':
                logo = logo.convert('RGB')
            qr_image.paste(logo, pos)

        return qr_image

    def generate(
        self,
        output_path: Optional[str] = None,
        logo_path: Optional[str] = None,
        custom_settings: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Path:
        """Generate QR code and save to file.

        Args:
            output_path: Output file path
            logo_path: Optional logo to embed in QR code
            custom_settings: Optional custom QR settings
            **kwargs: Additional arguments for prepare_data

        Returns:
            Path to saved QR code
        """
        try:
            # Prepare data
            data = self.prepare_data(**kwargs)
            self.logger.info("Generated data for QR code: %s...", data[:50])

            # Create QR code
            qr_image = self.create_qr_code(data, custom_settings)

            # Add logo if provided
            if logo_path:
                self.logger.info("Adding logo from %s", logo_path)
                qr_image = self.add_logo(qr_image, logo_path)

            # Determine output path
            output_path_obj: Path
            if not output_path:
                output_path_obj = self.config.get_output_path(
                    f"qr_{self._get_type_name()}_{self._get_timestamp()}.png"
                )
            else:
                output_path_obj = Path(output_path)

            # Ensure parent directory exists
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)

            # Save image
            qr_image.save(str(output_path_obj))
            self.logger.info("QR code saved to %s", output_path_obj)

            return output_path_obj

        except Exception as e:
            self.logger.error("Error generating QR code: %s", e, exc_info=True)
            raise

    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_type_name(self) -> str:
        """Get the QR code type name (e.g., 'url', 'wifi', 'sms')."""
        # Extract type from class name: URLQRGenerator -> url
        class_name = self.__class__.__name__
        # Remove 'QRGenerator' suffix and convert to lowercase
        type_name = class_name.replace('QRGenerator', '').lower()
        return type_name
