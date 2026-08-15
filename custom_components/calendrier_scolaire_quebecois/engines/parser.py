"""Moteur d'analyse pour l'extraction des événements de calendrier."""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)


class ParserEngine:
    """Analyse les sources de calendrier et extrait les événements."""

    def __init__(self, manager: Any) -> None:
        """Initialise le moteur d'analyse."""
        self.manager = manager
        self.parsers: Dict[str, Any] = {}

    async def parse(self, data: bytes, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyse les données d'une source."""
        _LOGGER.debug("Analyse de la source: %s", source.get("name"))

        # Détermine le type de fichier
        source_type = source.get("type", "direct_url")
        parser_type = source.get("parser_type", "generic")

        try:
            if source.get("url", "").lower().endswith(".pdf"):
                return await self._parse_pdf(data, source)
            elif source.get("url", "").lower().endswith(".ics"):
                return await self._parse_ical(data, source)
            else:
                return await self._parse_html(data, source)

        except Exception as err:
            _LOGGER.error(
                "Erreur lors de l'analyse de la source %s: %s", source.get("name"), err
            )
            return []

    async def parse_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyse un fichier PDF."""
        _LOGGER.info("Analyse du fichier PDF: %s", file_path)

        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return await self._parse_pdf(data, {"name": file_path})
        except Exception as err:
            _LOGGER.error("Error parsing PDF %s: %s", file_path, err)
            return []

    async def _parse_pdf(
        self, data: bytes, source: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Parse PDF content."""
        events = []

        try:
            # Try to use pdfplumber if available
            try:
                import pdfplumber

                pdf_io = __import__("io").BytesIO(data)

                with pdfplumber.open(pdf_io) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            page_events = await self._extract_events_from_text(
                                text, source
                            )
                            events.extend(page_events)

                return events

            except ImportError:
                _LOGGER.warning("pdfplumber not available, attempting OCR parsing")

                # Fall back to OCR if available
                if self.manager.ocr_engine:
                    events = await self.manager.ocr_engine.extract_from_pdf(
                        data, source
                    )

        except Exception as err:
            _LOGGER.error("Error parsing PDF: %s", err)

        return events

    async def _parse_ical(
        self, data: bytes, source: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Parse iCalendar format."""
        events = []

        try:
            import icalendar

            cal = icalendar.Calendar.from_ical(data)

            for component in cal.walk():
                if component.name == "VEVENT":
                    event = {
                        "title": str(component.get("summary", "Événement")),
                        "start": component.get("dtstart"),
                        "end": component.get("dtend"),
                        "description": str(component.get("description", "")),
                        "location": str(component.get("location", "")),
                        "source": source.get("name"),
                    }
                    events.append(event)

        except Exception as err:
            _LOGGER.error("Error parsing iCalendar: %s", err)

        return events

    async def _parse_html(
        self, data: bytes, source: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Parse HTML content."""
        events = []

        try:
            html_content = data.decode("utf-8", errors="ignore")
            return await self._extract_events_from_text(html_content, source)

        except Exception as err:
            _LOGGER.error("Error parsing HTML: %s", err)

        return events

    async def _extract_events_from_text(
        self, text: str, source: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract events from text using pattern matching."""
        events = []

        from ..const import DATE_PATTERNS, EVENT_KEYWORDS, HOLIDAY_KEYWORDS

        lines = text.split("\n")

        for line in lines:
            # Check if line contains event keywords
            is_event = any(
                keyword.lower() in line.lower() for keyword in EVENT_KEYWORDS
            )
            is_holiday = any(
                keyword.lower() in line.lower() for keyword in HOLIDAY_KEYWORDS
            )

            if is_event or is_holiday:
                # Try to extract dates
                dates = self._extract_dates(line)

                if dates:
                    event = {
                        "title": line.strip()[:100],
                        "start": dates[0] if dates else None,
                        "end": dates[1] if len(dates) > 1 else dates[0],
                        "is_holiday": is_holiday,
                        "source": source.get("name"),
                    }
                    if event["start"]:
                        events.append(event)

        return events

    def _extract_dates(self, text: str) -> List[datetime]:
        """Extract dates from text."""
        from ..const import DATE_PATTERNS

        dates = []

        for pattern in DATE_PATTERNS:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    # Try to parse different date formats
                    date_formats = [
                        "%d/%m/%Y",
                        "%d-%m-%Y",
                        "%d/%m/%y",
                        "%d-%m-%y",
                    ]

                    for fmt in date_formats:
                        try:
                            date = datetime.strptime(match, fmt)
                            dates.append(date)
                            break
                        except ValueError:
                            continue

                except Exception as err:
                    _LOGGER.debug("Error parsing date %s: %s", match, err)

        return dates
