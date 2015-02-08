"""
Django settings for OnQueue project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9$m6#aza)ictbav1r=tx%9!-g2j&9ea(gdt3*^a@fnz&l&0gd8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SEND_SMS = False

TEMPLATE_DEBUG = True
TOKEN = '1jg*fjfnHjf09nfkhnNFKS9n'

ALLOWED_HOSTS = []

#User model
AUTH_PROFILE_MODULE = 'clients.UserProfile'

HOST = "http://localhost"

# Application definition


DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


#List all the third party apps used in the project
THIRD_PARTY_APPS = (
    'tastypie',
    )

#list all the custom build apps
LOCAL_APPS = (
    'clients',
    'guests',
    )


INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OnQueue.urls'

WSGI_APPLICATION = 'OnQueue.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'myseconddb',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'onque',
            'PASSWORD': 'treehouse123',
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "clients/static"),
    # os.path.join(BASE_DIR, "guests/static"),

]

#Templates settings
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

csrf_value = '6x3Be4X2EIo31PMq6I1OQC2KbFejrS3y'

try:
    from local_settings import *
except ImportError:
    pass
    

