# ASGI асинхронный, для channels нужен он вместо WSGI

import os
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from apps.messenger.routing import websocket_urlpatterns as messenger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings.production')
application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AllowedHostsOriginValidator(  # Роутер для сокетов из messenger/routing
    AuthMiddlewareStack(
      URLRouter(messenger)
    )
  )
})
