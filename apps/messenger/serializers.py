from . import models

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class NewMessageSerializer(serializers.Serializer):
  chat_id = serializers.IntegerField()
  text = serializers.CharField(max_length=1000)

  def validate_chat_id(self, value: int) -> int:
    if not (chat := models.Chat.objects.filter(id=value)):  # Валидация на дурака
      raise ValidationError('Chat does not exist')

    self.chat = chat[0]
    return value
