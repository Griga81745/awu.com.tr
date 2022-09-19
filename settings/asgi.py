import os
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from apps.messenger.routing import websocket_urlpatterns as messenger

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(
      URLRouter(messenger)
    )
  )
})
