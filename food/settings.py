"""
Django settings for food project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from django.conf import settings
import cloudinary_storage
from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-v4h@qiqdh2+4@)fd+r!6@_=@+r13=n388x3fx-=7!tnia8&s9g')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'taggit',
    'storages',
    'hitcount',
    'cloudinary',
    'crispy_forms',
    'notifications',
    'import_export',
    'django_filters',
    'django_resized',
    'rest_framework',
    'django_countries',
    'cloudinary_storage',

    'api.apps.ApiConfig',
    'coupon.apps.CouponConfig',
    'orders.apps.OrdersConfig',
    'profil.apps.ProfilConfig',
    'refunds.apps.RefundsConfig',
    'website.apps.WebsiteConfig',
    'payments.apps.PaymentsConfig',
    'contacts.apps.ContactsConfig',
    'products.apps.ProductsConfig',
    'addresses.apps.AddressesConfig',
    'superadmin.apps.SuperadminConfig',
    'newsletter.apps.NewsletterConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'food.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'food.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE' : os.environ.get('ENGINE', 'django.db.backends.postgresql'),
        'NAME' : os.environ.get('NAME', ''),
        'USER' : os.environ.get('USER', ''),
        'PASSWORD' : os.environ.get('PASSWORD', ''),
        'HOST' : os.environ.get('HOST', ''),
        'PORT' : os.environ.get('PORT', '5432'),
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME', ''),
    'API_KEY' : os.environ.get('API_KEY', ''),
    'API_SECRET' : os.environ.get('API_SECRET', ''),
    'SECURE' : os.environ.get('SECURE', True),
}
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'cloudinary_storage.storage.MediaCloudinaryStorage')
"""

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = 'collectstatic/'
MEDIA_URL = '/food/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/food/media')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
    ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'nonameorg2021@gmail.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'Florineesse0808@')
# EMAIL_USE_LOCALTIME = True

HITCOUNT_HITS_PER_IP_LIMIT = 0

STRIPE_SECRET_KEY = ''
STRIPE_PUBLIC_KEY = ''

SITE_ID = 1

LOGIN_URL = 'login'



