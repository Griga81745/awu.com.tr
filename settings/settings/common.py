import environ
from pathlib import Path

env = environ.Env(
  DEBUG = (bool,False),
  SECRET_KEY = (str,'secret-key')
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env.read_env(BASE_DIR/'.env')

DEBUG = int(env('DEBUG')) 

INSTALLED_APPS = [
  'channels',
  'rest_framework',
  'taggit',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  'apps.we',
  'apps.users',
  'apps.posts',
  'apps.messenger.apps.MessengerConfig',
  'apps.api.apps.ApiConfig'
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'settings.urls'
ASGI_APPLICATION = 'settings.asgi.application'

TEMPLATES = [
  {
    "BACKEND": "django.template.backends.jinja2.Jinja2",
    "DIRS": [BASE_DIR / 'assets/templates'],
    "APP_DIRS": True,
    "OPTIONS": {
      "environment": "settings.jinja2.environment",
      "context_processors": [
        "django.contrib.messages.context_processors.messages",
      ],
    }
  },
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages'
      ],
      'libraries':{
        'utils':'templatetags.utils'
      }
    }
  }
]

STATICFILES_DIRS = [
  BASE_DIR / 'settings/static'
]

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
  }
]

LANGUAGE_CODE = 'tr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'assets/static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'assets/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'