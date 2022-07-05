# Тот же самый urls.py, но только для channels
# Если бы писали чат-комнату, то был бы параметр room_name
# А ещё название группы было бы равно room_name
# https://channels.readthedocs.io/en/stable/tutorial/part_2.html

from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
  re_path(r'^ws/chats/(?P<ticket>\w+)/$', consumers.ChatConsumer.as_asgi())
]
