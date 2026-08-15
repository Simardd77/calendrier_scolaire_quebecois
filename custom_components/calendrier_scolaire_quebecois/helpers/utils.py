"""Fonctions utilitaires pour Calendrier Scolaire Québécois."""

from __future__ import annotations

import logging
from datetime import datetime, date
from typing import Optional, Union, List, Dict, Any

_LOGGER = logging.getLogger(__name__)


def parse_date(date_string: str) -> Optional[datetime]:
    """Analyse une chaîne de date dans plusieurs formats."""
    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y-%m-%d",
        "%d %B %Y",
        "%d %b %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    return None


def format_date(date_obj: Union[datetime, date]) -> str:
    """Format a date object to string."""
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%d/%m/%Y")
    elif isinstance(date_obj, date):
        return date_obj.strftime("%d/%m/%Y")

    return str(date_obj)


def is_holiday(event: Dict[str, Any]) -> bool:
    """Check if an event is a holiday."""
    return event.get("is_holiday", False)


def get_event_duration_hours(
    event: Dict[str, Any],
) -> Optional[float]:
    """Calculate event duration in hours."""
    start = event.get("start")
    end = event.get("end")

    if not start or not end:
        return None

    if isinstance(start, str):
        start = datetime.fromisoformat(start)
    if isinstance(end, str):
        end = datetime.fromisoformat(end)

    if isinstance(start, datetime) and isinstance(end, datetime):
        delta = end - start
        return delta.total_seconds() / 3600

    return None


def filter_events_by_date(
    events: List[Dict[str, Any]], target_date: date
) -> List[Dict[str, Any]]:
    """Filter events by a specific date."""
    filtered = []

    for event in events:
        event_date = event.get("start")

        if isinstance(event_date, str):
            try:
                event_date = datetime.fromisoformat(event_date)
            except:
                continue

        if isinstance(event_date, datetime):
            event_date = event_date.date()

        if event_date == target_date:
            filtered.append(event)

    return filtered


def sort_events_by_date(
    events: List[Dict[str, Any]], reverse: bool = False
) -> List[Dict[str, Any]]:
    """Sort events by start date."""

    def get_sort_key(event):
        start = event.get("start")
        if isinstance(start, str):
            try:
                return datetime.fromisoformat(start)
            except:
                return datetime.now()
        return start or datetime.now()

    return sorted(events, key=get_sort_key, reverse=reverse)


def merge_event_sources(
    events_list: List[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Merge events from multiple sources."""
    merged = []
    seen_titles = set()

    for events in events_list:
        for event in events:
            # Avoid duplicates
            title = event.get("title", "").lower()
            if title and title not in seen_titles:
                merged.append(event)
                seen_titles.add(title)
            elif not title:
                merged.append(event)

    return sort_events_by_date(merged)
