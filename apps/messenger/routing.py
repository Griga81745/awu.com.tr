from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<peer_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]