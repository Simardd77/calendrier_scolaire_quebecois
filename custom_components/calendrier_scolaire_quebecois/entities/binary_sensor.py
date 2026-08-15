"""Entités capteur binaire pour Calendrier Scolaire Québécois."""

from __future__ import annotations

import logging
from typing import Any, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
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
    """Set up binary sensor entities."""
    manager: SchoolCalendarManager = hass.data[DOMAIN][entry.entry_id]["manager"]

    entities = [
        SchoolOpenSensor(manager, manager.coordinator),
        UpcomingEventSensor(manager, manager.coordinator),
        HolidaySensor(manager, manager.coordinator),
    ]

    async_add_entities(entities)


class SchoolOpenSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor indicating if school is open."""

    def __init__(self, manager: SchoolCalendarManager, coordinator: Any) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.manager = manager
        self._attr_name = f"{manager.name} - School Open"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_school_open"
        self._attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    @property
    def is_on(self) -> bool:
        """Return True if school is open."""
        try:
            # School is open if there are no holidays today
            from datetime import date

            today = date.today()
            holidays = [
                e
                for e in self.manager.events
                if e.get("is_holiday")
                and e.get("start")
                and e.get("start").date() == today
            ]

            return len(holidays) == 0

        except Exception as err:
            _LOGGER.error("Error checking if school is open: %s", err)

        return True


class UpcomingEventSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor indicating if there's an event today."""

    def __init__(self, manager: SchoolCalendarManager, coordinator: Any) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.manager = manager
        self._attr_name = f"{manager.name} - Event Today"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_event_today"
        self._attr_device_class = BinarySensorDeviceClass.MOTION

    @property
    def is_on(self) -> bool:
        """Return True if there's an event today."""
        try:
            from datetime import date

            today = date.today()
            today_events = [
                e
                for e in self.manager.events
                if e.get("start") and e.get("start").date() == today
            ]

            return len(today_events) > 0

        except Exception as err:
            _LOGGER.error("Error checking for events today: %s", err)

        return False


class HolidaySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor indicating if today is a holiday."""

    def __init__(self, manager: SchoolCalendarManager, coordinator: Any) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.manager = manager
        self._attr_name = f"{manager.name} - Holiday"
        self._attr_unique_id = f"{DOMAIN}_{manager.entry.entry_id}_holiday"
        self._attr_device_class = BinarySensorDeviceClass.SAFETY

    @property
    def is_on(self) -> bool:
        """Return True if today is a holiday."""
        try:
            from datetime import date

            today = date.today()
            holidays = [
                e
                for e in self.manager.events
                if e.get("is_holiday")
                and e.get("start")
                and e.get("start").date() == today
            ]

            return len(holidays) > 0

        except Exception as err:
            _LOGGER.error("Error checking for holidays: %s", err)

        return False
