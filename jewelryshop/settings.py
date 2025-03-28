import os
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'change_this_to_a_secure_key')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Installed Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'storages',  # Required for AWS S3 storage
    'store',  # Your custom app
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jewelryshop.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_preprocessors.store_menu',
                'store.context_preprocessors.cart_menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'jewelryshop.wsgi.application'

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')

# Database Configuration
USE_DYNAMODB = os.getenv('USE_DYNAMODB', 'False').lower() == 'true'
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'jewelryshop_data')

if USE_DYNAMODB:
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=AWS_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        print(f"✅ Connected to DynamoDB table: {DYNAMODB_TABLE_NAME}")
        DATABASES = {'default': {'ENGINE': 'django.db.backends.dummy'}}  # Django ORM does not support DynamoDB
    except (NoCredentialsError, PartialCredentialsError):
        print("⚠️ AWS Credentials are missing or invalid for DynamoDB! Reverting to SQLite.")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static & Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'jewelryshop/static']
STATIC_ROOT = BASE_DIR / 'static'

# Media Files Configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# AWS S3 Storage (For Media Files)
USE_AWS_STORAGE = os.getenv('USE_AWS_STORAGE', 'False').lower() == 'true'

if USE_AWS_STORAGE:
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'your-bucket-name')
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        print("⚠️ AWS credentials are missing! Check environment variables.")
    else:
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Django Sessions with DynamoDB
USE_DYNAMODB_SESSIONS = os.getenv('USE_DYNAMODB_SESSIONS', 'False').lower() == 'true'

if USE_DYNAMODB_SESSIONS and USE_DYNAMODB:
    SESSION_ENGINE = "django_dynamodb_sessions.backends.dynamodb"
    SESSION_DYNAMODB_TABLE = DYNAMODB_TABLE_NAME
