"""Tests unitaires du moteur de calendrier."""
import pytest
from datetime import datetime, timedelta
from custom_components.school_calendar_hub.engines.calendar_engine import (
    CalendarEngine,
)


class MockManager:
    """Gestionnaire factice pour les tests."""

    def __init__(self):
        self.region = "quebec"
        self.name = "Test School"

    def get_calendar_entity_id(self, name):
        return f"calendar.test_{name.lower()}"


@pytest.mark.asyncio
async def test_calendar_organize_events():
    """Test de l'organisation des événements."""
    manager = MockManager()
    engine = CalendarEngine(manager)

    events = [
        {
            "title": "Cours",
            "start": datetime.now(),
            "source": "École A",
            "is_holiday": False,
        },
        {
            "title": "Congé",
            "start": datetime.now(),
            "source": "École B",
            "is_holiday": True,
        },
    ]

    organized = engine._organize_events(events)

    assert "École A" in organized
    assert "Congés" in organized
    assert len(organized["École A"]) == 1
    assert len(organized["Congés"]) == 1


@pytest.mark.asyncio
async def test_calendar_get_upcoming_events():
    """Test de récupération des événements à venir."""
    manager = MockManager()
    engine = CalendarEngine(manager)

    now = datetime.now()
    events = [
        {
            "title": "Aujourd'hui",
            "start": now,
            "source": "École",
            "is_holiday": False,
        },
        {
            "title": "La semaine prochaine",
            "start": now + timedelta(days=7),
            "source": "École",
            "is_holiday": False,
        },
    ]

    await engine.async_update(events)
    upcoming = await engine.get_upcoming_events(days=7)

    assert len(upcoming) >= 1
