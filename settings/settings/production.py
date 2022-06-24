from .common import *

SECRET_KEY = int(env('DEBUG')) 

ALLOWED_HOSTS = ['*']



DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}
