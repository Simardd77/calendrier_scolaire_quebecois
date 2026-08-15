# Calendrier Scolaire Québécois pour Home Assistant

<p align="center">
  <img src="https://raw.githubusercontent.com/Simardd77/calendrier_scolaire_quebecois/main/custom_components/calendrier_scolaire_quebecois/brand/icon.png" alt="Logo" />
</p>

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub Release (latest by date)](https://img.shields.io/github/v/release/Simardd77/calendrier_scolaire_quebecois?style=for-the-badge)](https://github.com/Simardd77/calendrier_scolaire_quebecois)
[![GitHub License](https://img.shields.io/github/license/Simardd77/calendrier_scolaire_quebecois?style=for-the-badge)](LICENSE)

Une intégration Home Assistant pour gérer les calendriers scolaires québécois. Extrait les événements à partir des PDF, sites web et fichiers iCalendar grâce à l'OCR et à des moteurs d'analyse avancés.

## Fonctionnalités

- 📅 **Support multi-sources** : URLs directes, sites scolaires, fichiers iCalendar
- 🔍 **Moteur OCR** : Extrait les événements depuis les documents PDF avec Tesseract
- 🧠 **Moteur d'apprentissage** : Améliore la précision de l'analyse au fil du temps
- 📊 **Entités riches** : Calendrier, capteurs et capteurs binaires
- ⚡ **Appels de services** : Contrôle programmatique et personnalisation
- 🎯 **Découverte automatique** : Trouve les sources de calendrier à partir des sites scolaires

## Prérequis

- Home Assistant **2026.7.0** ou plus récent
- [HACS](https://hacs.xyz) installé

## Installation

### Via HACS (recommandé)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Simardd77&category=integration&repository=calendrier_scolaire_quebecois)

Après l'installation, redémarrez Home Assistant.

### Installation manuelle

1. Clonez ce dépôt
2. Copiez `custom_components/calendrier_scolaire_quebecois` dans le dossier `custom_components` de Home Assistant
3. Copiez le contenu de `www/` dans le dossier `www/` de Home Assistant (si applicable)
4. Redémarrez Home Assistant

## Configuration

### Configuration de base

1. Allez dans Paramètres → Appareils et services
2. Cliquez sur "Créer une intégration"
3. Recherchez "Calendrier Scolaire Québécois"
4. Configurez :
   - **Nom** : Nom descriptif pour votre calendrier
   - **Intervalle de rafraîchissement** : Fréquence de vérification des mises à jour (défaut : 3600 secondes)
   - **Activer l'OCR** : Utiliser l'OCR pour l'analyse PDF
   - **Mode d'apprentissage** : Activer l'amélioration automatique de l'analyseur

### Ajouter des sources de calendrier

Vous pouvez ajouter des sources de calendrier via :

1. **Interface du flux de configuration** - Pendant la configuration initiale
2. **Appel de service** - Utiliser `calendrier_scolaire_quebecois.add_source`
3. **Configuration** - Saisie manuelle dans `configuration.yaml`

#### Exemple d'appel de service

```yaml
service: calendrier_scolaire_quebecois.add_source
data:
  name: "Calendrier scolaire 2024"
  source_url: "https://example.com/calendar.pdf"
  source_type: "direct_url"
```

## Entités

### Entités de calendrier

- `calendar.calendrier_scolaire_quebecois_[nom]_[source]`
  - Affiche tous les événements d'une source spécifique

### Capteurs

- `sensor.calendrier_scolaire_quebecois_[nom]_total_events` - Nombre total d'événements
- `sensor.calendrier_scolaire_quebecois_[nom]_next_event` - Prochain événement à venir
- `sensor.calendrier_scolaire_quebecois_[nom]_upcoming_events_7_days` - Événements dans les 7 prochains jours
- `sensor.calendrier_scolaire_quebecois_[nom]_status` - État de l'intégration

### Capteurs binaires

- `binary_sensor.calendrier_scolaire_quebecois_[nom]_school_open` - École ouverte/fermée
- `binary_sensor.calendrier_scolaire_quebecois_[nom]_event_today` - Événement prévu aujourd'hui
- `binary_sensor.calendrier_scolaire_quebecois_[nom]_holiday` - Congé aujourd'hui

## Services

### Ajouter une source

```yaml
service: calendrier_scolaire_quebecois.add_source
data:
  name: "Nom de la source"
  source_url: "https://example.com/calendar.pdf"
  source_type: "direct_url"
  parser_type: "generic"
```

### Supprimer une source

```yaml
service: calendrier_scolaire_quebecois.remove_source
data:
  source_id: "source_123"
```

### Actualiser le calendrier

```yaml
service: calendrier_scolaire_quebecois.refresh_calendar
```

### Analyser un PDF

```yaml
service: calendrier_scolaire_quebecois.parse_pdf
data:
  file_path: "/path/to/calendar.pdf"
```

### Entraîner l'analyseur

```yaml
service: calendrier_scolaire_quebecois.train_parser
```

## Configuration avancée

### Activer le débogage avancé

```yaml
logger:
  logs:
    custom_components.calendrier_scolaire_quebecois: debug
```

### Configuration personnalisée du parseur

Créez des parseurs pour des écoles spécifiques dans `custom_components/calendrier_scolaire_quebecois/parsers/` :

```python
# parsers/my_school.py
class MySchoolParser:
    async def parse(self, data: bytes) -> List[Dict]:
        # Logique de parsing personnalisée
        pass
```

## Exigences

- Home Assistant 2026.1.0+
- Python 3.9+
- pytesseract (pour les fonctionnalités OCR)
- pdfplumber (pour l'analyse PDF)
- pillow (pour le traitement des images)

## Dépannage

### L'OCR ne fonctionne pas

Assurez-vous que Tesseract est installé :

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Téléchargez depuis : https://github.com/UB-Mannheim/tesseract/wiki
```

### Le PDF n'est pas analysé

1. Vérifiez les journaux : `logger.logs.custom_components.calendrier_scolaire_quebecois: debug`
2. Assurez-vous que le PDF n'est pas corrompu
3. Essayez une actualisation manuelle : Appelez `calendrier_scolaire_quebecois.refresh_calendar`

### Le moteur d'apprentissage ne s'entraîne pas

Un minimum de 10 événements est requis pour l'entraînement. Plus il y a de données, meilleure est la précision.

## Développement

### Configuration de l'environnement de développement

```bash
cd calendrier_scolaire_quebecois
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Exécution des tests

```bash
pytest tests/
```

## Contribution

Les contributions sont les bienvenues ! Veuillez :

1. Créer un fork du dépôt
2. Créer une branche de fonctionnalité
3. Faire vos modifications
4. Exécuter les tests
5. Soumettre une demande de pull

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE).

## Support

- 📧 **Problèmes** : [GitHub Issues](https://github.com/Simardd77/calendrier_scolaire_quebecois/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/Simardd77/calendrier_scolaire_quebecois/discussions)
- 📚 **Documentation** : [Documentation complète](docs/README.md)

## Crédits

- Conçu avec ❤️ pour Home Assistant
- Inspiré par la communauté Home Assistant
- OCR alimenté par Tesseract

---

**Fait avec ❤️ pour la communauté Home Assistant**
