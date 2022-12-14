from .common import *

SECRET_KEY = env('SECRET_KEY') 
ALLOWED_HOSTS = ['*']

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')  

CHANNEL_LAYERS = {
  'default': {
    'BACKEND': 'channels_redis.core.RedisChannelLayer',
    'CONFIG': {
      'hosts': [(REDIS_HOST, REDIS_PORT)]
    }
  }
}
