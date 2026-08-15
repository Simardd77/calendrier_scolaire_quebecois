"""Flux de configuration pour l'intégration Calendrier Scolaire Québécois."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_ENABLE_OCR,
    CONF_LEARNING_MODE,
    CONF_REFRESH_INTERVAL,
    CONF_SOURCE_TYPE,
    CONF_SOURCE_URL,
    DEFAULT_ENABLE_OCR,
    DEFAULT_LEARNING_MODE,
    DEFAULT_REFRESH_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

SOURCE_TYPES = ["direct_url", "school_website", "ical"]


class CalendrierScolaireQcConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gère le flux de configuration pour Calendrier Scolaire Québécois."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Gère l'étape initiale."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                name = user_input.get(CONF_NAME, "Calendrier Scolaire")
                source_url = user_input.get(CONF_SOURCE_URL, "")
                source_type = user_input.get(CONF_SOURCE_TYPE, "direct_url")

                # Vérifie les doublons
                await self.async_set_unique_id(name)
                self._abort_if_unique_id_configured()

                # Valide l'URL si fournie
                if source_url:
                    if not await self._validate_url(source_url):
                        errors["source_url"] = "cannot_connect"
                        raise CannotConnect("URL inaccessible")

                # Prépare les sources initiales
                sources = {}
                if source_url:
                    sources["source_0"] = {
                        "name": name,
                        "url": source_url,
                        "type": source_type,
                    }

                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_NAME: name,
                        CONF_SOURCE_URL: source_url,
                        CONF_SOURCE_TYPE: source_type,
                        CONF_REFRESH_INTERVAL: user_input.get(
                            CONF_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL
                        ),
                        CONF_ENABLE_OCR: user_input.get(
                            CONF_ENABLE_OCR, DEFAULT_ENABLE_OCR
                        ),
                        CONF_LEARNING_MODE: user_input.get(
                            CONF_LEARNING_MODE, DEFAULT_LEARNING_MODE
                        ),
                        "sources": sources,
                    },
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception as err:  # pylint: disable=broad-except
                errors["base"] = "unknown"
                _LOGGER.error("Erreur inconnue: %s", err)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Calendrier Scolaire"): str,
                vol.Optional(CONF_SOURCE_URL, default=""): str,
                vol.Optional(CONF_SOURCE_TYPE, default="direct_url"): vol.In(
                    SOURCE_TYPES
                ),
                vol.Optional(
                    CONF_REFRESH_INTERVAL, default=DEFAULT_REFRESH_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=86400)),
                vol.Optional(CONF_ENABLE_OCR, default=DEFAULT_ENABLE_OCR): bool,
                vol.Optional(CONF_LEARNING_MODE, default=DEFAULT_LEARNING_MODE): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={},
        )

    async def _validate_url(self, url: str) -> bool:
        """Valide qu'une URL est accessible."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(
                    url, timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    return resp.status < 400
        except Exception:
            return False

    async def async_step_import(self, import_data: Dict[str, Any]) -> FlowResult:
        """Importe une entrée de configuration depuis configuration.yaml."""
        return await self.async_step_user(import_data)


class CannotConnect(HomeAssistantError):
    """Erreur indiquant qu'on ne peut pas se connecter."""


class InvalidAuth(HomeAssistantError):
    """Erreur indiquant une authentification invalide."""
