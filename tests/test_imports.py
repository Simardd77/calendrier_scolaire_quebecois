"""Test rapide pour vérifier que les imports fonctionnent correctement."""
import sys
from pathlib import Path

# Ajouter le composant au path
component_path = Path(__file__).parent / "custom_components"
sys.path.insert(0, str(component_path))

try:
    print("Test des imports...")

    # Test des imports de base
    print("  ✓ Import de const...")
    from calendrier_scolaire_quebecois import const

    print("  ✓ Import de discovery...")
    from calendrier_scolaire_quebecois.engines.discovery import DiscoveryEngine

    print("  ✓ Import de parser...")
    from calendrier_scolaire_quebecois.engines.parser import ParserEngine

    print("  ✓ Import de ocr...")
    from calendrier_scolaire_quebecois.engines.ocr import OCREngine

    print("  ✓ Import de calendar_engine...")
    from calendrier_scolaire_quebecois.engines.calendar_engine import CalendarEngine

    print("  ✓ Import de learning...")
    from calendrier_scolaire_quebecois.engines.learning import LearningEngine

    print("  ✓ Import de manager...")
    from calendrier_scolaire_quebecois.core.manager import SchoolCalendarManager

    print("  ✓ Import des entités...")
    from calendrier_scolaire_quebecois.entities import calendar, sensor, binary_sensor

    print("  ✓ Import des helpers...")
    from calendrier_scolaire_quebecois.helpers import utils, config_validator

    print("\n✅ Tous les imports réussis ! Aucune dépendance circulaire détectée.")
    sys.exit(0)

except ImportError as e:
    print(f"\n❌ Erreur d'import : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
