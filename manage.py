#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import logging

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ ERROR: `python-dotenv` module is missing. Install it using: pip install python-dotenv")
    sys.exit(1)  # Exit if dotenv is not installed

def main():
    """Run administrative tasks with improved error handling."""

    # Define the base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Load environment variables from .env file if it exists
    dotenv_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print(f"✅ Loaded environment variables from {dotenv_path}")
    else:
        print("⚠️ WARNING: No .env file found. Ensure environment variables are set.")

    # Set default Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jewelryshop.settings")

    # Configure logging for better debugging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logging.error(
            "❌ ERROR: Couldn't import Django. Make sure it's installed and available on your PYTHONPATH. "
            "Did you forget to activate your virtual environment?"
        )
        sys.exit(1)

    logging.info("✅ Django management command executed successfully.")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
