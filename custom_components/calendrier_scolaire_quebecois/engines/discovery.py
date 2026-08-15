"""Moteur de découverte pour trouver les sources de calendrier."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import aiohttp

_LOGGER = logging.getLogger(__name__)


class DiscoveryEngine:
    """Découvre les sources de calendrier scolaire québécois."""

    def __init__(self, manager: Any) -> None:
        """Initialise le moteur de découverte."""
        self.manager = manager
        self.discovered_sources: Dict[str, Dict[str, Any]] = {}

    async def async_discover(self) -> Dict[str, Dict[str, Any]]:
        """Découvre les sources de calendrier disponibles."""
        _LOGGER.debug("Exécution de la découverte pour le Québec")

        sources = {}

        # Essaie de découvrir à partir des sources configurées
        if hasattr(self.manager.entry, "data") and "sources" in self.manager.entry.data:
            sources.update(self.manager.entry.data["sources"])

        # Ajoute les sources intégrées du Québec
        sources.update(await self._discover_quebec_sources())

        self.discovered_sources = sources
        return sources

    async def _discover_quebec_sources(self) -> Dict[str, Dict[str, Any]]:
        """Découvre les sources spécifiques au Québec."""
        sources = {}
        sources.update(self._get_quebec_sources())
        return sources

    def _get_quebec_sources(self) -> Dict[str, Dict[str, Any]]:
        """Obtient les sources courantes de calendrier scolaire du Québec."""
        return {
            "quebec_mels": {
                "name": "Ministère de l'Éducation du Québec",
                "type": "school_website",
                "url": "https://www.education.gouv.qc.ca",
                "description": "Calendrier officiel du Ministère de l'Éducation du Québec",
            },
            "quebec_commissions_scolaires": {
                "name": "Commissions Scolaires du Québec",
                "type": "school_website",
                "url": "https://www.quebec.ca",
                "description": "Calendriers des commissions scolaires du Québec",
            }
        }

    async def fetch_source(self, source: Dict[str, Any]) -> bytes:
        """Récupère les données d'une source de calendrier."""
        _LOGGER.debug("Récupération de la source: %s", source.get("name"))
        
        url = source.get("url")

        if not url:
            _LOGGER.warning("Aucune URL trouvée pour la source: %s", source.get("name"))
            return b""

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status == 200:
                        return await resp.read()
                    else:
                        _LOGGER.error(
                            "Échec de la récupération de la source %s: HTTP %d",
                            source.get("name"),
                            resp.status,
                        )
                        return b""
        except Exception as err:
            _LOGGER.error("Erreur lors de la récupération de la source %s: %s", source.get("name"), err)
            return b""

    async def auto_discover_from_website(self, url: str) -> List[Dict[str, Any]]:
        """Découvre automatiquement les sources de calendrier d'un site web."""
        _LOGGER.debug("Découverte automatique des sources à partir de: %s", url)

        sources = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status == 200:
                        content = await resp.text()

                        # Recherche les liens PDF liés aux calendriers
                        import re

                        pdf_pattern = r'href=["\'"]([^\'"]*\.pdf[^"\'"]*)["\'"]'
                        calendar_keywords = [
                            "calendar",
                            "calendrier",
                            "schedule",
                            "emploi",
                            "horaire",
                            "scolaire",
                        ]

                        for match in re.finditer(pdf_pattern, content, re.IGNORECASE):
                            pdf_url = match.group(1)

                            # Vérifie si l'URL contient des mots-clés de calendrier
                            if any(
                                keyword.lower() in pdf_url.lower()
                                for keyword in calendar_keywords
                            ):
                                sources.append(
                                    {
                                        "name": pdf_url.split("/")[-1],
                                        "type": "direct_url",
                                        "url": pdf_url
                                        if pdf_url.startswith("http")
                                        else url.rstrip("/") + "/" + pdf_url.lstrip("/"),
                                        "discovered": True,
                                    }
                                )

        except Exception as err:
            _LOGGER.error("Erreur lors de la découverte automatique à partir de %s: %s", url, err)

        return sources
