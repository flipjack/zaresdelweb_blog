"""Production settings and globals."""
from base import *
from privado import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zaresdelaweb_blog', # The following settings are not used with sqlite3:
        'USER': 'zares',
        'PASSWORD': PASSWORD_DB_PRIV,
        'HOST': '',# Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',# Set to empty string for default.
    }
}
########## END DATABASE CONFIGURATION

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['www.zaresdelaweb.com','zaresdelaweb.com']
########## END HOST CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = SECRET_KEY_PRIV
########## END SECRET CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION
SITE_URL = 'http://www.zaresdelaweb.com'

DISQUS_URL= 'http://www.zaresdelaweb.com'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = EMAIL_USUARIO_PRIV,
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD_PRIV,
EMAIL_PORT = 587

