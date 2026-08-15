"""Intégration Calendrier Scolaire Québécois pour Home Assistant."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_ENTITY_ID,
    ATTR_FILE_PATH,
    ATTR_SOURCE_ID,
    CONF_LEARNING_MODE,
    CONF_NAME,
    DOMAIN,
    PLATFORMS,
    SERVICE_ADD_SOURCE,
    SERVICE_PARSE_PDF,
    SERVICE_REFRESH_CALENDAR,
    SERVICE_REMOVE_SOURCE,
    SERVICE_TRAIN_PARSER,
)
from .core.manager import SchoolCalendarManager

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

# Schémas de services
SCHEMA_ADD_SOURCE = cv.OBJECT
SCHEMA_REMOVE_SOURCE = cv.OBJECT
SCHEMA_REFRESH_CALENDAR = cv.OBJECT
SCHEMA_PARSE_PDF = cv.OBJECT
SCHEMA_TRAIN_PARSER = cv.OBJECT


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configure le composant Calendrier Scolaire Québécois."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure Calendrier Scolaire Québécois depuis une entrée de configuration."""
    _LOGGER.info("Configuration de Calendrier Scolaire Québécois: %s", entry.data.get(CONF_NAME))
    
    manager = SchoolCalendarManager(hass, entry)
    
    try:
        await manager.async_init()
    except Exception as err:
        _LOGGER.error("Erreur lors de l'initialisation du gestionnaire: %s", err)
        raise ConfigEntryNotReady(f"Erreur lors de l'initialisation: {err}") from err
    
    hass.data[DOMAIN][entry.entry_id] = {
        "manager": manager,
    }
    
    # Configure les plateformes
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Enregistre les services
    await _async_register_services(hass, manager)
    
    # Écoute les changements de configuration
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharge une entrée de configuration."""
    _LOGGER.info("Déchargement de Calendrier Scolaire Québécois: %s", entry.data.get(CONF_NAME))
    
    data = hass.data[DOMAIN][entry.entry_id]
    manager = data["manager"]
    
    await manager.async_shutdown()
    
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Recharge une entrée de configuration."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def _async_register_services(
    hass: HomeAssistant, manager: SchoolCalendarManager
) -> None:
    """Enregistre les services pour Calendrier Scolaire Québécois."""
    
    async def handle_add_source(call: ServiceCall) -> None:
        """Gère le service d'ajout de source."""
        source_data = call.data
        await manager.add_source(source_data)
        _LOGGER.info("Source ajoutée: %s", source_data.get("name"))
    
    async def handle_remove_source(call: ServiceCall) -> None:
        """Gère le service de suppression de source."""
        source_id = call.data.get(ATTR_SOURCE_ID)
        await manager.remove_source(source_id)
        _LOGGER.info("Source supprimée: %s", source_id)
    
    async def handle_refresh_calendar(call: ServiceCall) -> None:
        """Gère le service d'actualisation du calendrier."""
        await manager.async_refresh()
        _LOGGER.info("Calendrier actualisé")
    
    async def handle_parse_pdf(call: ServiceCall) -> None:
        """Gère le service d'analyse PDF."""
        file_path = call.data.get(ATTR_FILE_PATH)
        events = await manager.parse_pdf(file_path)
        _LOGGER.info("PDF analysé: %d événements extraits", len(events))
    
    async def handle_train_parser(call: ServiceCall) -> None:
        """Gère le service d'entraînement de l'analyseur."""
        if manager.learning_engine:
            await manager.learning_engine.train()
            _LOGGER.info("Analyseur entraîné")
    
    # Enregistre tous les services
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_SOURCE,
        handle_add_source,
        schema=SCHEMA_ADD_SOURCE,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_REMOVE_SOURCE,
        handle_remove_source,
        schema=SCHEMA_REMOVE_SOURCE,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH_CALENDAR,
        handle_refresh_calendar,
        schema=SCHEMA_REFRESH_CALENDAR,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_PARSE_PDF,
        handle_parse_pdf,
        schema=SCHEMA_PARSE_PDF,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_TRAIN_PARSER,
        handle_train_parser,
        schema=SCHEMA_TRAIN_PARSER,
    )
    
    _LOGGER.debug("Services registered")
