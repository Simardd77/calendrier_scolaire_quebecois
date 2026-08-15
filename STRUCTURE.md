# Calendrier Scolaire Québécois - Aperçu de la structure du projet

## Structure complète du répertoire

```
calendrier_scolaire_quebecois/
├── custom_components/
│   └── calendrier_scolaire_quebecois/          # Intégration principale
│       ├── __init__.py                        # Configuration et services
│       ├── config_flow.py                     # Interface de configuration
│       ├── const.py                           # Constantes et réglages
│       ├── manifest.json                      # Métadonnées de l'intégration
│       ├── services.yaml                      # Définition des services
│       ├── strings.json                       # Chaînes localisées
│       │
│       ├── brand/
│       │   └── icon.png                       # Icône de l'intégration
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   └── manager.py                     # Orchestrateur principal
│       │
│       ├── engines/                           # Moteurs de traitement
│       │   ├── __init__.py
│       │   ├── discovery.py                   # Découverte des sources
│       │   ├── parser.py                      # Analyse PDF/HTML/iCal
│       │   ├── ocr.py                         # OCR Tesseract
│       │   ├── calendar_engine.py              # Organisation des événements
│       │   └── learning.py                    # Améliorations via apprentissage
│       │
│       ├── entities/                          # Entités Home Assistant
│       │   ├── __init__.py
│       │   ├── calendar.py                    # Entités calendrier
│       │   ├── sensor.py                      # Entités capteurs
│       │   └── binary_sensor.py               # Entités capteurs binaires
│       │
│       ├── helpers/                           # Fonctions utilitaires
│       │   ├── __init__.py
│       │   ├── utils.py                       # Fonctions d'aide
│       │   └── config_validator.py            # Validation de configuration
│       │
│       └── translations/
│           └── en.json                        # Traductions anglaises
│
├── docs/                                      # Documentation technique
│   ├── README.md
│   └── ...
│
├── tests/                                     # Suite de tests
│   ├── __init__.py
│   ├── conftest.py                           # Configuration des tests
│   ├── test_parser.py                        # Tests du parseur
│   ├── test_calendar_engine.py                # Tests du calendrier
│   └── test_discovery.py                     # Tests de découverte
│
├── .github/workflows/                         # GitHub Actions
│   ├── release.yml                           # Automatisation de version
│   └── validate.yml                          # Validation CI/CD
│
├── README.md                                  # Documentation principale
├── DEVELOPMENT.md                             # Guide développeur
├── FAQ.md                                     # Questions fréquentes
├── LICENSE                                    # Licence MIT
├── hacs.json                                  # Configuration HACS
├── .gitignore                                 # Fichier gitignore
└── requirements.txt                           # Dépendances de développement
```

## Aperçu des composants

### Composants principaux

| Composant | Rôle | Statut |
|-----------|------|--------|
| **Manager** | Orchestration des moteurs | ✅ Terminé |
| **Discovery Engine** | Trouve les sources de calendrier | ✅ Terminé |
| **Parser Engine** | Extrait les événements | ✅ Terminé |
| **OCR Engine** | Extraction de texte via Tesseract | ✅ Terminé |
| **Calendar Engine** | Organise et gère les événements | ✅ Terminé |
| **Learning Engine** | Améliore la précision du parseur | ✅ Terminé |

### Entités

| Type d'entité | Nombre | Statut |
|---------------|--------|--------|
| Calendrier | Dynamique par source | ✅ Terminé |
| Capteurs | 4 (Total, Prochain, À venir, État) | ✅ Terminé |
| Capteurs binaires | 3 (Ouverte, Événement du jour, Congé) | ✅ Terminé |

### Fonctionnalités implémentées

- ✅ Support multi-sources
- ✅ Analyse PDF avec OCR
- ✅ Support iCalendar
- ✅ Analyse HTML
- ✅ Découverte de sources pour le Québec
- ✅ Moteur d'apprentissage
- ✅ Appels de services pour automatisation
- ✅ Flux de configuration
- ✅ Suite de tests
- ✅ CI/CD
- ✅ Documentation complète

## Prochaines personnalisations

1. **Ajouter des sources québécoises**
2. **Améliorer les parseurs**
3. **Créer un tableau de bord frontend**
4. **Ajouter des notifications**
5. **Créer une API**
6. **Ajouter un module famille**
7. **Améliorer le moteur d'apprentissage**

## Exemple d'utilisation

### Ajouter une source
```yaml
service: calendrier_scolaire_quebecois.add_source
data:
  name: "Mon école 2024"
  source_url: "https://example.com/calendar.pdf"
  source_type: "direct_url"
```

### Rafraîchir le calendrier
```yaml
service: calendrier_scolaire_quebecois.refresh_calendar
```

### Entraîner le parseur
```yaml
service: calendrier_scolaire_quebecois.train_parser
```

## Structure de la documentation

1. **README.md** - Documentation grand public
2. **DEVELOPMENT.md** - Guide développeur
3. **FAQ.md** - Questions et dépannage
4. **docs/** - Spécifications techniques
5. **Commentaires du code** - Documentation inline

---

**Statut de l'intégration** : ✅ **FONCTIONNELLE**

Prête pour l'installation, les tests et le déploiement !
