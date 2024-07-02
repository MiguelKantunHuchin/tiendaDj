from .base import *
from firebase_admin import credentials, auth
import firebase_admin

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_secret("DB_NAME"),
        "USER": get_secret("USER"),
        "PASSWORD": get_secret("PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOOT = BASE_DIR / "media"

cred = credentials.Certificate("fbkey.json")
firebase_admin.initialize_app(cred)
