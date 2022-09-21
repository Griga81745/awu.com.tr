import os
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'
asgi_application = get_asgi_application()

from apps.messenger.routing import websocket_urlpatterns as messenger

application = ProtocolTypeRouter({
  'http': asgi_application,
  'websocket': AuthMiddlewareStack(
    URLRouter(messenger)
  )
})
