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

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*w5khesoy7s+mx&6=@m$q*s(n$^86gvfyacktfn+=n30tqj2!-'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
BASE_URL = 'https://api.vendescrow.com'
ALLOWED_HOSTS = ['*']
MANAGERS = ('Vendescrow', "vendescrow@gmail.com")
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
    'django_celery_beat',
    'django_celery_results',
]

# Third-party
INSTALLED_APPS += [
    'phonenumber_field',
    'crispy_forms',
    'rest_framework',
    'corsheaders',
    'widget_tweaks',
    'markdown_deux',
    'pagedown',
    # 'channels',
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
    'coins',
    'referrals',
    'notifications',
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

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# WSGI_APPLICATION = 'vendescrow.wsgi.application'
ASGI_APPLICATION = 'vendescrow.asgi.application'

# heroku config - gives latest redis credentials
CELERY_BROKER_URL = 'redis://:p2196718fddb40d4cae789847f5ce368fb6245550cb84eef2a45d41dd30ea202a@ec2-34-195-152-131.compute-1.amazonaws.com:7999'
BROKER_URL = 'redis://:p2196718fddb40d4cae789847f5ce368fb6245550cb84eef2a45d41dd30ea202a@ec2-34-195-152-131.compute-1.amazonaws.com:7999'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_PASSWORD = "p2196718fddb40d4cae789847f5ce368fb6245550cb84eef2a45d41dd30ea202a"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ddnoo6ngtlfdjh',
        'USER': 'hlhopjqfqylfho',
        'PASSWORD': '667740ba95a4a31a508725df2f39e7f18a21f0af2a0a4c8c7acdb25678e58ac6',
        'HOST': 'ec2-54-235-108-217.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

CHANNEL_LAYERS = {
    # queue of messages
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ["redis://:p2196718fddb40d4cae789847f5ce368fb6245550cb84eef2a45d41dd30ea202a@ec2-3-209-155-39.compute-1.amazonaws.com:12589"],
            'symmetric_encryption_keys': [SECRET_KEY],
        },
    },
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