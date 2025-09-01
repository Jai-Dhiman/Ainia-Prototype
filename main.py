"""Entry point for the Ainia Adventure Stories application."""

import sys
import os

# Add src to path for package imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from multimodal_app import main

if __name__ == "__main__":
    main()
