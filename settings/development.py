from .common import *

SECRET_KEY = 'secret-key'
ALLOWED_HOSTS = ['*']

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

CHANNEL_LAYERS = {
  'default': {
    'BACKEND': 'channels.layers.InMemoryChannelLayer'
  }
}
