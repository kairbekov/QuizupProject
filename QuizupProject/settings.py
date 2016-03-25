"""
Django settings for QuizupProject project.

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
SECRET_KEY = '&yihzfa%eixz4iydbyf%jzyua25vbch986--4ss1b&-4wzk^ka'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', 'entalapp.kz', '185.22.67.17', 'www.entalapp.kz']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'push_notifications',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'QuizupProject.urls'

WSGI_APPLICATION = 'QuizupProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'EntalappDB',
        'USER': 'abuka',
        'PASSWORD': 'Kbtu2012',
        'HOST': '185.22.67.17',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'EntalappDB',
#         'USER': 'root',
#         'PASSWORD': 'pRU0pkiBYf',
#         'HOST': 'mysql21760-env-3315080.j.dnr.kz',
#         'PORT': '3306',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

PUSH_NOTIFICATIONS_SETTINGS = {
        "GCM_API_KEY": "AIzaSyBcgNGFRtyMYt_sfK9MROFE5WqK3-LQsFs",
        "GCM_POST_URL": "https://android.googleapis.com/gcm/send",
        "APNS_CERTIFICATE": "C:/Users/abuka/Desktop/cunkey.pem",
}

#GCM_APIKEY = "AIzaSyBcgNGFRtyMYt_sfK9MROFE5WqK3-LQsFs"

SOUTH_MIGRATION_MODULES = {"push_notifications": "push_notifications.south_migrations"}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)
