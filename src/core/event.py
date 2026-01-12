"""Calendar event QR code generator."""

from typing import Optional
from datetime import datetime
from .base import BaseQRGenerator


class EventQRGenerator(BaseQRGenerator):
    """Generate QR codes for calendar events."""

    # pylint: disable=arguments-differ  # Keyword-only params are more specific than base **kwargs
    def prepare_data(
        self,
        *,
        title: str,
        start_time: datetime,
        end_time: datetime,
        location: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> str:
        """Prepare calendar event data.

        Args:
            title: Event title
            start_time: Event start time
            end_time: Event end time
            location: Event location
            description: Event description

        Returns:
            vCalendar formatted string
        """
        # Format dates in iCalendar format (YYYYMMDDTHHMMSS)
        start_str = start_time.strftime("%Y%m%dT%H%M%S")
        end_str = end_time.strftime("%Y%m%dT%H%M%S")

        vevent_lines = [
            "BEGIN:VEVENT",
            f"SUMMARY:{title}",
            f"DTSTART:{start_str}",
            f"DTEND:{end_str}",
        ]

        if location:
            vevent_lines.append(f"LOCATION:{location}")

        if description:
            vevent_lines.append(f"DESCRIPTION:{description}")

        vevent_lines.append("END:VEVENT")

        vevent_data = "\n".join(vevent_lines)

        self.logger.debug("Prepared event data: %s", title)
        return vevent_data
