"""
WSGI config for jewelryshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
import logging
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Define the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jewelryshop.settings")

# Logging Configuration for WSGI Errors
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

try:
    application = get_wsgi_application()
    logging.info("✅ WSGI application loaded successfully.")
except Exception as e:
    logging.error(f"❌ WSGI application failed to load: {e}")
    raise e
