# ASGI асинхронный, для channels нужен он вместо WSGI

import os
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'

# from apps.messenger.routing import websocket_urlpatterns as messenger
# from .middlewares import TokenAuthMiddlewareStack


application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  # 'websocket': AllowedHostsOriginValidator(  # Роутер для сокетов из messenger/routing
  #   TokenAuthMiddlewareStack(
  #     URLRouter(messenger)
  #   )
  # )
})
