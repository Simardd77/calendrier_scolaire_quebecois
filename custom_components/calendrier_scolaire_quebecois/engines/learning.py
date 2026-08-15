"""Moteur d'apprentissage pour améliorer la précision de l'analyseur."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__)


class LearningEngine:
    """Moteur d'apprentissage automatique pour améliorer la précision d'analyse."""

    def __init__(self, manager: Any) -> None:
        """Initialise le moteur d'apprentissage."""
        self.manager = manager
        self.training_data: List[Dict[str, Any]] = []
        self.models: Dict[str, Any] = {}
        self.state_file = Path(self.manager.hass.config.path(
            f".{self.manager.name}_learning.json"
        ))
        self._load_state()

    async def async_process_events(
        self, events: List[Dict[str, Any]]
    ) -> None:
        """Process events for learning."""
        _LOGGER.debug("Processing %d events for learning", len(events))

        for event in events:
            # Add metadata for training
            event["processed_at"] = datetime.now().isoformat()
            event["confidence"] = event.get("confidence", 0.5)

            self.training_data.append(event)

        # Keep only recent training data
        if len(self.training_data) > 1000:
            self.training_data = self.training_data[-1000:]

    async def improve_events(
        self, events: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Improve event parsing using learned patterns."""
        _LOGGER.debug("Improving %d events using learned patterns", len(events))

        improved_events = []

        for event in events:
            improved_event = event.copy()

            # Apply learned corrections
            if self.training_data:
                improved_event = await self._apply_learned_patterns(
                    improved_event
                )

            improved_events.append(improved_event)

        return improved_events

    async def _apply_learned_patterns(
        self, event: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply learned patterns to improve event."""
        # This is a simplified implementation
        # In a real ML system, you would use actual models here

        # Example: improve title formatting
        title = event.get("title", "")
        if title:
            # Apply common title corrections learned from data
            corrections = {
                "classe": "Class",
                "réunion": "Meeting",
                "examén": "Exam",
                "excursion": "Excursion",
            }

            for wrong, correct in corrections.items():
                if wrong.lower() in title.lower():
                    event["confidence"] = event.get("confidence", 0.5) + 0.1
                    break

        return event

    async def train(self) -> None:
        """Train the learning models."""
        _LOGGER.info("Training learning models with %d samples", 
                    len(self.training_data))

        if len(self.training_data) < 10:
            _LOGGER.warning(
                "Not enough training data (%d samples), need at least 10",
                len(self.training_data),
            )
            return

        try:
            # Here you would train actual ML models
            # For now, just compute some statistics

            # Analyze title patterns
            titles = [e.get("title", "") for e in self.training_data]
            title_patterns = self._extract_patterns(titles)

            self.models["title_patterns"] = title_patterns

            # Analyze date patterns
            dates = [e.get("start") for e in self.training_data if e.get("start")]
            date_patterns = self._extract_patterns([str(d) for d in dates])

            self.models["date_patterns"] = date_patterns

            # Save state
            await self.save_state()

            _LOGGER.info("Learning models trained successfully")

        except Exception as err:
            _LOGGER.error("Error training learning models: %s", err)

    def _extract_patterns(self, texts: List[str]) -> Dict[str, int]:
        """Extract common patterns from texts."""
        patterns = {}

        for text in texts:
            if not text:
                continue

            # Count word frequencies
            words = text.lower().split()
            for word in words:
                patterns[word] = patterns.get(word, 0) + 1

        # Return top patterns
        return dict(
            sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:20]
        )

    async def save_state(self) -> None:
        """Save learning engine state to file."""
        try:
            state = {
                "training_data": self.training_data[-100:],  # Keep last 100
                "models": self.models,
                "saved_at": datetime.now().isoformat(),
            }

            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=2, default=str)

            _LOGGER.debug("Learning engine state saved")

        except Exception as err:
            _LOGGER.error("Error saving learning engine state: %s", err)

    def _load_state(self) -> None:
        """Load learning engine state from file."""
        try:
            if self.state_file.exists():
                with open(self.state_file, "r") as f:
                    state = json.load(f)

                self.training_data = state.get("training_data", [])
                self.models = state.get("models", {})

                _LOGGER.debug(
                    "Learning engine state loaded with %d training samples",
                    len(self.training_data),
                )

        except Exception as err:
            _LOGGER.error("Error loading learning engine state: %s", err)
