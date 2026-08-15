"""Validation de configuration pour Calendrier Scolaire Québécois."""
from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import config_validation as cv

DOMAIN_SCHEMA = vol.Schema(
    {
        vol.Required("name"): cv.string,
        vol.Optional("sources", default=[]): vol.All(
            cv.ensure_list,
            [
                {
                    vol.Required("name"): cv.string,
                    vol.Required("url"): cv.url,
                    vol.Optional("type", default="direct_url"): cv.string,
                }
            ],
        ),
        vol.Optional("refresh_interval", default=3600): cv.positive_int,
        vol.Optional("enable_ocr", default=True): cv.boolean,
        vol.Optional("learning_mode", default=True): cv.boolean,
    }
)


def validate_source_config(source: dict) -> dict:
    """Validate source configuration."""
    required_fields = ["name", "url"]

    for field in required_fields:
        if field not in source:
            raise vol.Invalid(f"Missing required field: {field}")

    return source
