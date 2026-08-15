"""Tests unitaires du moteur de découverte."""
import pytest
from custom_components.school_calendar_hub.engines.discovery import (
    DiscoveryEngine,
)


class MockManager:
    """Gestionnaire factice pour les tests."""

    def __init__(self):
        self.region = "quebec"
        self.entry = type("obj", (object,), {"data": {}})()


@pytest.mark.asyncio
async def test_discovery_quebec_sources():
    """Test de découverte des sources du Québec."""
    manager = MockManager()
    engine = DiscoveryEngine(manager)

    sources = engine._get_quebec_sources()

    assert "quebec_mels" in sources
    assert "Ministère de l'Éducation du Québec" in sources["quebec_mels"]["name"]


@pytest.mark.asyncio
async def test_discovery_async_discover():
    """Test de découverte asynchrone."""
    manager = MockManager()
    engine = DiscoveryEngine(manager)

    sources = await engine.async_discover()

    assert len(sources) > 0
