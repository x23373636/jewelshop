#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from dotenv import load_dotenv

def main():
    """Run administrative tasks with improved error handling."""
    
    # Define the base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Load environment variables from .env file
    dotenv_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Set default Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jewelryshop.settings")

    # Configure logging for better error visibility
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logging.error(
            "❌ Couldn't import Django. Make sure it's installed and available on your PYTHONPATH. "
            "Did you forget to activate your virtual environment?"
        )
        raise ImportError("Django is missing or virtual environment is not activated.") from exc

    logging.info("✅ Django management command executed successfully.")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
