# Calendrier Scolaire Québécois - Guide de développement

## Vue d'ensemble de l'architecture

```
Utilisateur (Home Assistant)
    ↓
ConfigFlow (configuration)
    ↓
Manager (orchestration)
    ↓
┌─────────────────────────────────────────┐
│  Discovery Engine                       │
│  - Trouve les sources de calendrier     │
│  - Découverte automatique des sites     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Parser Engine                          │
│  - Analyse les PDF, iCalendar, HTML     │
│  - Extrait les événements               │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  OCR Engine (optionnel)                 │
│  - Extraction de texte depuis images    │
│  - Reconnaissance via Tesseract          │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Calendar Engine                        │
│  - Organise les événements              │
│  - Gère les entités de calendrier       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Learning Engine (optionnel)            │
│  - Améliore la précision                │
│  - Reconnaissance de motifs             │
└─────────────────────────────────────────┘
    ↓
Entités (calendrier, capteurs, capteurs binaires)
    ↓
Tableau de bord Home Assistant
```

## Structure des fichiers

```
custom_components/school_calendar_hub/
├── __init__.py                  # Configuration principale
├── config_flow.py              # Flux de configuration
├── const.py                    # Constantes
├── manifest.json               # Métadonnées de l'intégration
├── services.yaml               # Définition des services
├── strings.json                # Chaînes localisées
│
├── core/
│   ├── __init__.py
│   └── manager.py              # Orchestration principale
│
├── engines/
│   ├── __init__.py
│   ├── discovery.py            # Découverte de sources
│   ├── parser.py               # Analyse PDF/HTML/iCal
│   ├── ocr.py                  # OCR
│   ├── calendar_engine.py       # Gestion du calendrier
│   └── learning.py             # Moteur d'apprentissage
│
├── entities/
│   ├── __init__.py
│   ├── calendar.py             # Entités calendrier
│   ├── sensor.py               # Entités capteurs
│   └── binary_sensor.py        # Entités capteurs binaires
│
└── helpers/
    ├── __init__.py
    ├── utils.py                # Fonctions utilitaires
    └── config_validator.py     # Validation de configuration
```

## Ajouter un nouveau parseur

Créez un nouveau fichier dans `custom_components/school_calendar_hub/engines/parsers/` :

```python
# parsers/my_school.py
class MySchoolParser:
    """Parseur pour le format de calendrier d'une école."""

    async def parse(self, data: bytes, source: dict) -> list:
        """Analyse les données du calendrier."""
        events = []
        # Logique de parsing ici
        return events
```

## Ajouter un nouveau contexte régional

Cette intégration est conçue pour le Québec. La personnalisation se fait par ajout de sources spécifiques ou de parseurs ciblés, sans passer par plusieurs régions.

## Tests

```bash
# Tous les tests
pytest tests/

# Fichier de test précis
pytest tests/test_parser.py

# Avec couverture
pytest --cov=custom_components/school_calendar_hub tests/
```

## Débogage

Activez le journal de débogage :

```yaml
logger:
  logs:
    custom_components.school_calendar_hub: debug
    custom_components.school_calendar_hub.engines: debug
    custom_components.school_calendar_hub.core: debug
```

## Tâches courantes

### Ajouter un nouveau type d'entité

1. Créez `entities/new_entity.py`
2. Ajoutez la fonction d'installation : `async_setup_entry()`
3. Créez la classe d'entité en héritant de la base adaptée
4. Ajoutez la plateforme dans `PLATFORMS` du fichier `const.py`

### Améliorer la précision du parseur

1. Collectez des PDF et exemples de sites
2. Exécutez le service `school_calendar_hub.parse_pdf`
3. Vérifiez les événements extraits
4. Mettez à jour les motifs dans `const.py`
5. Entraînez le moteur d'apprentissage : `school_calendar_hub.train_parser`

## Optimisation des performances

- Mettez en cache les PDF analysés
- Limitez les données d'entraînement aux échantillons récents
- Utilisez des tâches de fond pour les opérations lourdes
- Implémentez un contrôle de débit pour les sources web

## Considérations de sécurité

- Validez toutes les URLs externes
- Nettoyez les entrées utilisateur
- Ne stockez pas de données sensibles
- Utilisez des valeurs par défaut sécurisées
- Mettez en place un rate limiting

## Règles de contribution

1. Suivez le guide de style PEP 8
2. Ajoutez des types
3. Documentez les fonctions
4. Écrivez des tests pour les nouvelles fonctionnalités
5. Mettez à jour la documentation

## Ressources

- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [Home Assistant Integration Documentation](https://developers.home-assistant.io/docs/development_index/)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
