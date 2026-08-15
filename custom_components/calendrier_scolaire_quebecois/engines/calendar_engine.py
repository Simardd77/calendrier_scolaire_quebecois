"""Moteur de calendrier pour la gestion des entités de calendrier."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__)


class CalendarEngine:
    """Gère les entités de calendrier et les événements."""

    def __init__(self, manager: Any) -> None:
        """Initialise le moteur de calendrier."""
        self.manager = manager
        self.calendars: Dict[str, CalendarData] = {}
        self.events: List[Dict[str, Any]] = []

    async def async_update(self, events: List[Dict[str, Any]]) -> None:
        """Update calendar with new events."""
        _LOGGER.debug("Updating calendars with %d events", len(events))

        self.events = events

        # Organize events by calendar
        calendar_events = self._organize_events(events)

        # Update or create calendars
        for calendar_name, events_list in calendar_events.items():
            if calendar_name not in self.calendars:
                self.calendars[calendar_name] = CalendarData(
                    name=calendar_name,
                    entity_id=self.manager.get_calendar_entity_id(calendar_name),
                )

            self.calendars[calendar_name].events = events_list

    def _organize_events(
        self, events: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Organize events by calendar."""
        calendars = {}

        for event in events:
            # Determine calendar name
            source = event.get("source", "General")
            is_holiday = event.get("is_holiday", False)

            calendar_name = "Holidays" if is_holiday else source

            if calendar_name not in calendars:
                calendars[calendar_name] = []

            calendars[calendar_name].append(event)

        return calendars

    async def get_events(
        self,
        calendar_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Get events for a specific calendar or date range."""
        events = self.events

        if calendar_name:
            calendar = self.calendars.get(calendar_name)
            if calendar:
                events = calendar.events

        if start_date or end_date:
            filtered = []
            for event in events:
                event_start = event.get("start")
                if isinstance(event_start, str):
                    try:
                        event_start = datetime.fromisoformat(event_start)
                    except:
                        continue

                if start_date and event_start < start_date:
                    continue
                if end_date and event_start > end_date:
                    continue

                filtered.append(event)

            events = filtered

        return events

    async def get_upcoming_events(
        self, days: int = 7, calendar_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get upcoming events."""
        now = datetime.now()
        end_date = now + timedelta(days=days)

        return await self.get_events(
            calendar_name=calendar_name, start_date=now, end_date=end_date
        )

    async def add_event(self, calendar_name: str, event: Dict[str, Any]) -> None:
        """Add an event to a calendar."""
        _LOGGER.debug("Adding event to calendar %s", calendar_name)

        if calendar_name not in self.calendars:
            self.calendars[calendar_name] = CalendarData(
                name=calendar_name,
                entity_id=self.manager.get_calendar_entity_id(calendar_name),
            )

        self.calendars[calendar_name].events.append(event)
        self.events.append(event)

    async def remove_event(self, event_id: str) -> None:
        """Remove an event."""
        _LOGGER.debug("Removing event: %s", event_id)

        self.events = [e for e in self.events if e.get("id") != event_id]

        for calendar in self.calendars.values():
            calendar.events = [e for e in calendar.events if e.get("id") != event_id]

    def get_calendar_info(self, calendar_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a calendar."""
        calendar = self.calendars.get(calendar_name)
        if calendar:
            return {
                "name": calendar.name,
                "entity_id": calendar.entity_id,
                "event_count": len(calendar.events),
                "last_updated": calendar.last_updated,
            }
        return None


class CalendarData:
    """Data class for a calendar."""

    def __init__(self, name: str, entity_id: str) -> None:
        """Initialize calendar data."""
        self.name = name
        self.entity_id = entity_id
        self.events: List[Dict[str, Any]] = []
        self.last_updated = datetime.now()
        self.color = "blue"

    def update_events(self, events: List[Dict[str, Any]]) -> None:
        """Update events."""
        self.events = events
        self.last_updated = datetime.now()
