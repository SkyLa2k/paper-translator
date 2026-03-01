"""Main entry point for Paper Translator."""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui.main_window import main

if __name__ == "__main__":
    main()