"""Gestionnaire principal pour Calendrier Scolaire Québécois."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import (
    CONF_ENABLE_OCR,
    CONF_LEARNING_MODE,
    CONF_NAME,
    CONF_REFRESH_INTERVAL,
    DOMAIN,
    UPDATE_INTERVAL_NORMAL,
)
from ..engines.discovery import DiscoveryEngine
from ..engines.parser import ParserEngine
from ..engines.ocr import OCREngine
from ..engines.calendar_engine import CalendarEngine
from ..engines.learning import LearningEngine

_LOGGER = logging.getLogger(__name__)


class SchoolCalendarManager:
    """Gère toutes les opérations de calendrier scolaire."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialise le gestionnaire."""
        self.hass = hass
        self.entry = entry
        self.name = entry.data.get(CONF_NAME, "Calendrier Scolaire")
        self.refresh_interval = entry.data.get(
            CONF_REFRESH_INTERVAL, UPDATE_INTERVAL_NORMAL
        )
        self.enable_ocr = entry.data.get(CONF_ENABLE_OCR, True)
        self.learning_mode = entry.data.get(CONF_LEARNING_MODE, True)

        # Initialize engines
        self.discovery_engine = DiscoveryEngine(self)
        self.parser_engine = ParserEngine(self)
        self.ocr_engine = OCREngine(self) if self.enable_ocr else None
        self.calendar_engine = CalendarEngine(self)
        self.learning_engine = LearningEngine(self) if self.learning_mode else None

        # Data storage
        self.sources: Dict[str, Any] = {}
        self.events: List[Dict[str, Any]] = []
        self.calendars: Dict[str, Any] = {}

        # Coordinator
        self.coordinator: Optional[DataUpdateCoordinator] = None

    async def async_init(self) -> None:
        """Initialize the manager."""
        _LOGGER.debug("Initializing School Calendar Manager")

        # Initialize coordinator
        self.coordinator = DataUpdateCoordinator(
            self.hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.name}",
            update_method=self.async_update,
            update_interval=timedelta(seconds=self.refresh_interval),
        )

        # Load initial data
        await self.coordinator.async_config_entry_first_refresh()

    async def async_update(self) -> None:
        """Update calendar data."""
        _LOGGER.debug("Updating calendars for %s", self.name)

        try:
            # Discover new sources
            new_sources = await self.discovery_engine.async_discover()
            self.sources.update(new_sources)

            # Parse all sources
            all_events = []
            for source_id, source in self.sources.items():
                events = await self._process_source(source)
                all_events.extend(events)

            # Update calendar engine
            self.events = all_events
            await self.calendar_engine.async_update(self.events)

            # Train learning engine if enabled
            if self.learning_engine:
                await self.learning_engine.async_process_events(self.events)

            _LOGGER.info(
                "Calendar update completed: %d events for %s",
                len(self.events),
                self.name,
            )

        except Exception as err:
            _LOGGER.error("Error updating calendars: %s", err)
            raise UpdateFailed(f"Error updating calendars: {err}") from err

    async def _process_source(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process a single source and extract events."""
        _LOGGER.debug("Processing source: %s", source.get("name"))

        try:
            # Get source data (download PDF or fetch from URL)
            source_data = await self.discovery_engine.fetch_source(source)

            # Parse the data
            events = await self.parser_engine.parse(source_data, source)

            # Apply learning if available
            if self.learning_engine:
                events = await self.learning_engine.improve_events(events)

            return events

        except Exception as err:
            _LOGGER.error("Error processing source %s: %s", source.get("name"), err)
            return []

    async def add_source(self, source_data: Dict[str, Any]) -> None:
        """Add a new calendar source."""
        _LOGGER.info("Adding source: %s", source_data.get("name"))
        source_id = source_data.get("id", str(len(self.sources)))
        self.sources[source_id] = source_data

        # Store in config entry
        self._save_sources_to_config()

        # Trigger update
        if self.coordinator:
            await self.coordinator.async_refresh()

    async def remove_source(self, source_id: str) -> None:
        """Remove a calendar source."""
        _LOGGER.info("Removing source: %s", source_id)
        if source_id in self.sources:
            del self.sources[source_id]
            self._save_sources_to_config()

            # Trigger update
            if self.coordinator:
                await self.coordinator.async_refresh()

    async def async_refresh(self) -> None:
        """Manually refresh calendars."""
        if self.coordinator:
            await self.coordinator.async_refresh()

    async def parse_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a PDF file and extract events."""
        _LOGGER.info("Parsing PDF: %s", file_path)
        return await self.parser_engine.parse_pdf(file_path)

    async def async_shutdown(self) -> None:
        """Shutdown the manager."""
        _LOGGER.debug("Shutting down School Calendar Manager")
        if self.learning_engine:
            await self.learning_engine.save_state()

    def _save_sources_to_config(self) -> None:
        """Save sources to config entry."""
        self.hass.config_entries.async_update_entry(
            self.entry,
            data={**self.entry.data, "sources": self.sources},
        )

    def get_calendar_entity_id(self, calendar_name: str) -> str:
        """Get the entity ID for a calendar."""
        safe_name = calendar_name.lower().replace(" ", "_")
        return f"calendar.{DOMAIN}_{self.name.lower()}_{safe_name}"
