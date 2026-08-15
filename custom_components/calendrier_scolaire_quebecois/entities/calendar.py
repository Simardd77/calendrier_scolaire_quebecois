"""Entité de calendrier pour Calendrier Scolaire Québécois."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..core.manager import SchoolCalendarManager

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configure les entités de calendrier."""
    manager: SchoolCalendarManager = hass.data[DOMAIN][entry.entry_id]["manager"]

    entities = []

    # Crée une entité de calendrier pour chaque calendrier découvert
    for calendar_name in manager.calendar_engine.calendars:
        entities.append(
            SchoolCalendarEntity(
                manager=manager,
                calendar_name=calendar_name,
                coordinator=manager.coordinator,
            )
        )

    async_add_entities(entities)


class SchoolCalendarEntity(CoordinatorEntity, CalendarEntity):
    """Représente un calendrier scolaire québécois."""

    def __init__(
        self,
        manager: SchoolCalendarManager,
        calendar_name: str,
        coordinator: Any,
    ) -> None:
        """Initialize the calendar entity."""
        super().__init__(coordinator)
        self.manager = manager
        self.calendar_name = calendar_name
        self._attr_name = f"{manager.name} - {calendar_name}"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_{calendar_name}"

    @property
    def name(self) -> str:
        """Return the name of the calendar."""
        return self._attr_name

    @property
    def unique_id(self) -> str:
        """Return a unique id."""
        return self._attr_unique_id

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within the specified date range."""
        events = []

        try:
            calendar_events = (
                await self.manager.calendar_engine.get_events(
                    calendar_name=self.calendar_name,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            for event in calendar_events:
                cal_event = CalendarEvent(
                    summary=event.get("title", "Event"),
                    start=event.get("start"),
                    end=event.get("end", event.get("start")),
                    description=event.get("description", ""),
                    location=event.get("location", ""),
                )
                events.append(cal_event)

        except Exception as err:
            _LOGGER.error("Error getting calendar events: %s", err)

        return events

    async def async_create_event(
        self,
        summary: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
    ) -> None:
        """Create a calendar event."""
        event = {
            "title": summary,
            "start": start_date,
            "end": end_date or start_date,
            "description": description or "",
            "location": location or "",
            "source": self.calendar_name,
        }

        await self.manager.calendar_engine.add_event(self.calendar_name, event)

    @property
    def event(self) -> Optional[CalendarEvent]:
        """Return the next upcoming event."""
        try:
            upcoming = self.manager.calendar_engine.calendars[
                self.calendar_name
            ].events

            if upcoming:
                next_event = upcoming[0]
                return CalendarEvent(
                    summary=next_event.get("title", "Event"),
                    start=next_event.get("start"),
                    end=next_event.get("end", next_event.get("start")),
                )

        except Exception as err:
            _LOGGER.error("Error getting next event: %s", err)

        return None
