"""Entry point for the Ainia Adventure Stories application."""

import sys
import os
import argparse

# Add src to path for package imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point with support for different app versions."""
    parser = argparse.ArgumentParser(description='Run Ainia Adventure Stories')
    parser.add_argument(
        '--enhanced', 
        action='store_true', 
        help='Run the enhanced multi-question version with adaptive difficulty'
    )
    
    args = parser.parse_args()
    
    print("🏰 Starting Ainia Adventure Stories...")
    from ainia.apps.app import main as app_main
    app_main()

if __name__ == "__main__":
    main()
