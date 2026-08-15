"""Quick test to verify imports work correctly."""
import sys
from pathlib import Path

# Add the component to path
component_path = Path(__file__).parent / "custom_components"
sys.path.insert(0, str(component_path))

try:
    print("Testing imports...")
    
    # Test basic imports
    print("  ✓ Importing const...")
    from school_calendar_hub import const
    
    print("  ✓ Importing discovery...")
    from school_calendar_hub.engines.discovery import DiscoveryEngine
    
    print("  ✓ Importing parser...")
    from school_calendar_hub.engines.parser import ParserEngine
    
    print("  ✓ Importing ocr...")
    from school_calendar_hub.engines.ocr import OCREngine
    
    print("  ✓ Importing calendar_engine...")
    from school_calendar_hub.engines.calendar_engine import CalendarEngine
    
    print("  ✓ Importing learning...")
    from school_calendar_hub.engines.learning import LearningEngine
    
    print("  ✓ Importing manager...")
    from school_calendar_hub.core.manager import SchoolCalendarManager
    
    print("  ✓ Importing entities...")
    from school_calendar_hub.entities import calendar, sensor, binary_sensor
    
    print("  ✓ Importing helpers...")
    from school_calendar_hub.helpers import utils, config_validator
    
    print("\n✅ All imports successful! No circular dependencies detected.")
    sys.exit(0)
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
