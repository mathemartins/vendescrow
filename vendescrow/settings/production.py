"""
Django settings for vendescrow project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import requests

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*w5khesoy7s+mx&6=@m$q*s(n$^86gvfyacktfn+=n30tqj2!-'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
BASE_URL = 'https://vendescrow.herokuapp.com'
ALLOWED_HOSTS = ['*']
MANAGERS = ('Vend Escrow', "vendescrow@gmail.com")
ADMINS = MANAGERS


# Application Defaults
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_jenkins',
]

# Third-party
INSTALLED_APPS += [
    'django_celery_beat',
    'phonenumber_field',
    'crispy_forms',
    'rest_framework',
    'corsheaders',
    'widget_tweaks',
    'markdown_deux',
    'pagedown',
]

# User created
INSTALLED_APPS += [
    'accounts',
    'wallets',
    'posts',
    'rates',
    'p2p',
    'fiatwallet',
    'mono',
    'transactions',
]


X_FRAME_OPTIONS = 'SAMEORIGIN'
FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vendescrow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vendescrow.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd752pnbc65ahih',
        'USER': 'wknwnqpwqahqgm',
        'PASSWORD': 'd7792ba7ee53d797f5ccbecc662c2c5bc850c14a442912ded023f1f127fe6ca2',
        'HOST': 'ec2-54-235-108-217.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

from vendescrow.cloudinary_settings import *
from vendescrow.restconf.main import *
from vendescrow.email_settings import *

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/account/<username>/'
LOGOUT_REDIRECT_URL = '/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media_root")
PROTECTED_ROOT = os.path.join(BASE_DIR, "static", "protected_media")

CORS_ORIGIN_ALLOW_ALL = True
HOST_SCHEME = "http://"
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False

from vendescrow.ssl_config import *

proxies = {
    "http": os.environ['QUOTAGUARDSTATIC_URL'],
    "https": os.environ['QUOTAGUARDSTATIC_URL'],
}

response = requests.get('http://ip.quotaguard.com/', proxies=proxies)
print(response.text)