from . import serializers, models
from . import mixins as custom_mixins
from django.contrib.auth import get_user_model

from typing import Dict
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

User = get_user_model()


class ChatConsumer(custom_mixins.JsonParser, JsonWebsocketConsumer):

  def connect(self) -> None:
    self.user: User = self.scope['user']

    if not self.user.is_authenticated:
      self.close(code=403)

    self.group_name = str(self.user.id)

    async_to_sync(self.channel_layer.group_add)(
      self.group_name,
      self.channel_name
    )

    self.accept()

  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      self.group_name,
      self.channel_name
    )

  def receive_json(self, content):
    serializer = serializers.NewMessageSerializer(data=content)

    if not serializer.is_valid():
      return self.send_json({'status': 'error', **serializer.errors})

    chat: models.Chat = serializer.chat
    all_participants = chat.participants.all()

    if self.user not in all_participants:
      return self.send_json({'status': 'error', 'message': 'User does not participate the chat'})

    text = serializer.validated_data['text']

    models.Message.objects.create(
      sender=self.user,
      chat=chat,
      text=text
    )

    for participant in all_participants:
      if participant == self.user:
        continue

      async_to_sync(self.channel_layer.group_send)(
        str(participant.id),
        {
          'type': 'chat_message',
          'chat_id': chat.id,
          'text': text
        }
      )

    self.send_json({'status': 'ok'})

  def chat_message(self, event: Dict) -> None:
    self.send_json({'event': 'new_message', **event})
