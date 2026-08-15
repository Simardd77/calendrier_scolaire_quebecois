"""Tests unitaires du moteur d'analyse."""
import pytest
from custom_components.school_calendar_hub.engines.parser import ParserEngine


class MockManager:
    """Gestionnaire factice pour les tests."""

    def __init__(self):
        self.region = "quebec"
        self.ocr_engine = None
        self.parser_engine = None


@pytest.mark.asyncio
async def test_parser_extract_dates():
    """Test d'extraction de dates."""
    manager = MockManager()
    parser = ParserEngine(manager)

    text = "L'école est fermée le 15/08/2024"
    dates = parser._extract_dates(text)

    assert len(dates) > 0
    assert dates[0].day == 15
    assert dates[0].month == 8
    assert dates[0].year == 2024


@pytest.mark.asyncio
async def test_parser_extract_events_from_text():
    """Test d'extraction d'événements à partir du texte."""
    manager = MockManager()
    parser = ParserEngine(manager)

    text = """
    Calendrier scolaire 2024

    Les cours débutent le 05/09/2024
    Congé : 25/12/2024 - 02/01/2025
    Réunion : 10/10/2024
    """

    events = await parser._extract_events_from_text(
        text, {"name": "École Test"}
    )

    assert len(events) >= 1
