"""Conftest for tests."""
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from unittest.mock import MagicMock, patch


@pytest.fixture
def hass():
    """Provide a mock Home Assistant instance."""
    hass = MagicMock(spec=HomeAssistant)
    hass.config.path = MagicMock(return_value="/test/path")
    return hass


@pytest.fixture
def config_entry():
    """Provide a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        "name": "Calendrier de test",
        "refresh_interval": 3600,
        "enable_ocr": True,
        "learning_mode": True,
    }
    return entry
