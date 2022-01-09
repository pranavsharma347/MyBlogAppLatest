"""
Django settings for BlogApplicationProject project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import dj_database_url
import django_heroku
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-59s81kzek0y9ix*qt$!j4czq7&rvj1q=zqu6gq_v(ca^jj-64o'

STATIC_DIR=os.path.join(BASE_DIR,'static')
TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'BlogApp',
    #for social app
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #provide google authentication
    'allauth.socialaccount.providers.google',
    
    #provide for package social-auth-app-django
    'social_django'  
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

ROOT_URLCONF = 'BlogApplicationProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    #add this for social_auth_app_django
    
    'social_core.backends.google.GoogleOAuth2',
    
    'social_core.backends.facebook.FacebookOAuth2',

    
]


SITE_ID = 3

LOGIN_REDIRECT_URL='/home/'
# Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'SCOPE':[
#             'profile',
#             'email',
#         ],
            
#         'AUTH_PARAMS':{ 
#             'access_type':'online',
#         }
#     }
# }

WSGI_APPLICATION = 'BlogApplicationProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME':'blogapp',
#         'USER':'admin',
#         'PASSWORD':'pranav12',
#         'HOST':'blogapp.cz7x3kl5ouyb.ap-northeast-1.rds.amazonaws.com',
#         'PORT':'3306'
#     }
# }

DATABASES={
    'default':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'blogdatabase',
        'USER':'postgres',
        'PASSWORD':'f4Jrm0zLLK9PBWpcQG7p',
        'HOST': 'herokublog.cz7x3kl5ouyb.ap-northeast-1.rds.amazonaws.com',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

WHITENOISE_USE_FINDERS = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS=[STATIC_DIR]
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR:'danger'
}

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 
STATICFILES_STORAGE = 'whitenoise.storage.GzipManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='javashrm@gmail.com'
EMAIL_HOST_PASSWORD='qjgikqjsyzcjxxxn'
EMAIL_USE_TLS=True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "962623803808-mlin25ce8g2j3puh522knah04a3ggtcg.apps.googleusercontent.com"         # Client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"  # Client Secret

SOCIAL_AUTH_FACEBOOK_KEY='255338473350263'
SOCIAL_AUTH_FACEBOOK_SECRET='65c82217c421920df6a5178494f76719'




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())

