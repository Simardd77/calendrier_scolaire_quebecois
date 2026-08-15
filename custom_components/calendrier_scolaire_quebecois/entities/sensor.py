"""Entités capteur pour Calendrier Scolaire Québécois."""
from __future__ import annotations

import logging
from typing import Any, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
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
    """Set up sensor entities."""
    manager: SchoolCalendarManager = hass.data[DOMAIN][entry.entry_id]["manager"]

    entities = [
        EventCountSensor(manager, manager.coordinator),
        NextEventSensor(manager, manager.coordinator),
        UpcomingEventsSensor(manager, manager.coordinator),
        CalendarStatusSensor(manager, manager.coordinator),
    ]

    async_add_entities(entities)


class EventCountSensor(CoordinatorEntity, SensorEntity):
    """Sensor for total event count."""

    def __init__(self, manager: SchoolCalendarManager, coordinator: Any) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.manager = manager
        self._attr_name = f"{manager.name} - Total Events"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_event_count"
        self._attr_native_unit_of_measurement = "events"
        self._attr_state_class = SensorStateClass.TOTAL

    @property
    def native_value(self) -> int:
        """Return the number of events."""
        return len(self.manager.events)


class NextEventSensor(CoordinatorEntity, SensorEntity):
    """Sensor for next upcoming event."""

    def __init__(self, manager: SchoolCalendarManager, coordinator: Any) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.manager = manager
        self._attr_name = f"{manager.name} - Next Event"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_next_event"

    @property
    def native_value(self) -> Optional[str]:
        """Return the next event."""
        try:
            upcoming = self.manager.calendar_engine.get_upcoming_events(days=30)
            if upcoming:
                return upcoming[0].get("title", "Unknown Event")
        except Exception as err:
            _LOGGER.error("Error getting next event: %s", err)

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        attrs = {}

        try:
            upcoming = self.manager.calendar_engine.get_upcoming_events(days=30)
            if upcoming:
                first_event = upcoming[0]
                attrs["start"] = first_event.get("start")
                attrs["end"] = first_event.get("end")
                attrs["source"] = first_event.get("source")

        except Exception as err:
            _LOGGER.error("Error getting event details: %s", err)

        return attrs


class UpcomingEventsSensor(CoordinatorEntity, SensorEntity):
    """Sensor for upcoming events count."""

    def __init__(self, manager: SchoolCalendarManager, coordinator: Any) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.manager = manager
        self._attr_name = f"{manager.name} - Upcoming Events (7 days)"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_upcoming_count"
        self._attr_native_unit_of_measurement = "events"

    @property
    def native_value(self) -> int:
        """Return count of upcoming events."""
        try:
            upcoming = self.manager.calendar_engine.get_upcoming_events(days=7)
            return len(upcoming)
        except Exception as err:
            _LOGGER.error("Error counting upcoming events: %s", err)

        return 0


class CalendarStatusSensor(CoordinatorEntity, SensorEntity):
    """Sensor for calendar integration status."""

    def __init__(self, manager: SchoolCalendarManager, coordinator: Any) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.manager = manager
        self._attr_name = f"{manager.name} - Status"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_status"

    @property
    def native_value(self) -> str:
        """Return the status."""
        if not self.manager.sources:
            return "no_sources"

        if not self.manager.events:
            return "no_events"

        return "ready"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "sources_count": len(self.manager.sources),
            "calendars_count": len(self.manager.calendar_engine.calendars),
            "events_count": len(self.manager.events),
            "last_updated": self.coordinator.last_update_success,
        }
