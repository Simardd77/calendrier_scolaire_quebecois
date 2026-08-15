"""Constantes pour l'intégration Calendrier Scolaire Québécois."""

DOMAIN = "calendrier_scolaire_quebecois"
VERSION = "1.0.0"

# Clés d'entrée de configuration
CONF_NAME = "name"
CONF_SOURCES = "sources"
CONF_REFRESH_INTERVAL = "refresh_interval"
CONF_ENABLE_OCR = "enable_ocr"
CONF_LEARNING_MODE = "learning_mode"

# Configuration de la source
CONF_SOURCE_NAME = "source_name"
CONF_SOURCE_URL = "source_url"
CONF_SOURCE_TYPE = "source_type"  # "direct_url", "school_website", "ical"
CONF_PARSER_TYPE = "parser_type"  # "generic", "specific", "ai"

# Noms des services
SERVICE_ADD_SOURCE = "add_source"
SERVICE_REMOVE_SOURCE = "remove_source"
SERVICE_REFRESH_CALENDAR = "refresh_calendar"
SERVICE_PARSE_PDF = "parse_pdf"
SERVICE_TRAIN_PARSER = "train_parser"

# Attributs
ATTR_SOURCE_ID = "source_id"
ATTR_FILE_PATH = "file_path"
ATTR_EXTRACTED_EVENTS = "extracted_events"
ATTR_CONFIDENCE = "confidence"
ATTR_ENTITY_ID = "entity_id"

# Plateformes
PLATFORMS = ["calendar", "sensor", "binary_sensor"]

# Valeurs par défaut
DEFAULT_REFRESH_INTERVAL = 3600  # 1 heure en secondes
DEFAULT_SCAN_INTERVAL = 60  # 1 minute
DEFAULT_ENABLE_OCR = True
DEFAULT_LEARNING_MODE = True

# Configuration OCR
OCR_ENABLED = True
OCR_LANGUAGE = ["fra", "eng"]  # Français et anglais
OCR_CONFIDENCE_THRESHOLD = 0.6

# Motifs regex pour extraction de dates/événements
DATE_PATTERNS = [
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",  # DD/MM/YYYY ou DD-MM-YYYY
    r"\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}",  # Date complète
]

HOLIDAY_KEYWORDS = [
    "vacances",
    "congé",
    "fermeture",
    "fermé",
    "fériés",
    "relâche",
    "congé pédagogique",
    "semaine de congé",
]

EVENT_KEYWORDS = [
    "classe",
    "école",
    "rentrée",
    "réunion",
    "excursion",
    "examen",
    "test",
    "présentation",
    "projet",
]

# Chemins de stockage
STORAGE_CACHE_DIR = "cache"
STORAGE_PDFS_DIR = "pdfs"
STORAGE_DATA_DIR = "data"

# Seuils du moteur d'apprentissage
LEARNING_MIN_SAMPLES = 10
LEARNING_CONFIDENCE_THRESHOLD = 0.75

# Intervalles de mise à jour (secondes)
UPDATE_INTERVAL_FAST = 300  # 5 minutes
UPDATE_INTERVAL_NORMAL = 3600  # 1 heure
UPDATE_INTERVAL_SLOW = 86400  # 1 jour

# Gestion des erreurs
MAX_RETRIES = 3
RETRY_DELAY = 60  # secondes

# Logging
LOG_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
