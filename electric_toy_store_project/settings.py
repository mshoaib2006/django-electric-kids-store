import os
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env file
load_dotenv(BASE_DIR / ".env")


# =========================
# Security
# =========================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-this-in-production"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "http://127.0.0.1:8001,http://localhost:8001"
    ).split(",")
    if origin.strip()
]


# =========================
# Applications
# =========================

INSTALLED_APPS = [
    "cloudinary_storage",
    "cloudinary",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "store",
]


# =========================
# Middleware
# =========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise middleware can serve static files on Render.
    # Storage is kept simple below to avoid collectstatic compression missing-file issue.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "electric_toy_store_project.urls"


# =========================
# Templates
# =========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "store.context_processors.cart_context",
            ],
        },
    },
]


WSGI_APPLICATION = "electric_toy_store_project.wsgi.application"


# =========================
# Database
# If DATABASE_URL exists → Neon PostgreSQL
# If DATABASE_URL missing → SQLite fallback
# =========================

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =========================
# Password validation
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================
# Language / Time
# =========================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Karachi"

USE_I18N = True

USE_TZ = True


# =========================
# Static files
# CSS / JS / fixed website images
# =========================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Compatibility for packages that still read old STATICFILES_STORAGE.
# We keep static storage simple to avoid Cloudinary/WhiteNoise compression missing-file error.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


# =========================
# Media files
# Product/category images uploaded from admin
# If CLOUDINARY_URL exists → Cloudinary
# If missing → local media folder
# =========================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")

if CLOUDINARY_URL:
    parsed_cloudinary = urlparse(CLOUDINARY_URL)

    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": parsed_cloudinary.hostname,
        "API_KEY": parsed_cloudinary.username,
        "API_SECRET": parsed_cloudinary.password,
    }

    DEFAULT_FILE_STORAGE_BACKEND = "cloudinary_storage.storage.MediaCloudinaryStorage"
else:
    CLOUDINARY_STORAGE = {}

    DEFAULT_FILE_STORAGE_BACKEND = "django.core.files.storage.FileSystemStorage"

# Compatibility for packages that still read old DEFAULT_FILE_STORAGE.
DEFAULT_FILE_STORAGE = DEFAULT_FILE_STORAGE_BACKEND

STORAGES = {
    "default": {
        "BACKEND": DEFAULT_FILE_STORAGE_BACKEND,
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# =========================
# Default primary key
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================
# Login / Logout
# =========================

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"

SESSION_ENGINE = "django.contrib.sessions.backends.db"


# =========================
# Render / HTTPS settings
# =========================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG


# =========================
# Store public details
# =========================

STORE_NAME = "Raffay Kids Corner"

STORE_PHONE_DISPLAY = "+92 370 1670717"

WHATSAPP_NUMBER = "923701670717"

STORE_EMAIL = "rafaykidscorner@gmail.com"

STORE_LOCATION = "Pakistan"