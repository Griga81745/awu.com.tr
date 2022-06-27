from . import serializers, models
from . import mixins as custom_mixins
from django.contrib.auth import get_user_model

from typing import Dict
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

User = get_user_model()


class ChatConsumer(custom_mixins.JsonParser, JsonWebsocketConsumer):
  ''' Консьюмер, который обрабатывает все сокет-подключения '''

  def connect(self) -> None:
    ''' Когда пользователь подключился '''

    self.user: User = self.scope['user']  # Вытащить из скоупа (типа как request)
    # Оно автоматом AuthMiddlewareStack из asgi.py логинит пользователя дефолтным путём через куки

    if not self.user.is_authenticated:
      return self.close(code=403)  # Если пользователя не вышло получить из куки

    self.group_name = str(self.user.id)  # Название группы
    # Так как сообщение приходит одному пользователю, вся группа будет состоять из одного пользователя
    # на момент, когда пользователь подключился. Сообщение будет отправляться в группу пользователя и потом пересылаться через сокет
    # Если бы писали чат-комнату, то group_name был бы названием чата и все пользователи в группе получали бы сообщение (то о чём я говорила)

    async_to_sync(self.channel_layer.group_add)(  # Добавить пользователя в группу (если группа с пользователем существует, значит пользователь онлайн)
      self.group_name,
      self.channel_name
    )

    self.accept()  # Принять соединение

  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(  # Если пользователь отключился от сокета, значит его нужно удалить из группы (оффлайн)
      self.group_name,
      self.channel_name
    )

  def receive_json(self, content):
    serializer = serializers.NewMessageSerializer(data=content)  # DRF для валидации входящего JSON, ещё DRF нужен будет в проекте для REST'а

    if not serializer.is_valid():
      return self.send_json({'status': 'error', **serializer.errors})  # Отправить по сокету ошибки, frontend ловит status: либо ок, либо error. Тект ошибки также можно использовать

    chat: models.Chat = serializer.chat
    all_participants = chat.participants.all()  # Получить всех участников чата (будут всего 2)

    if self.user not in all_participants:  # Если пользователя нет в чате (валидация на дурака)
      return self.send_json({'status': 'error', 'message': 'User does not participate the chat'})

    text = serializer.validated_data['text']

    models.Message.objects.create(
      sender=self.user,
      chat=chat,
      text=text
    )

    for participant in all_participants:

      if participant == self.user:  # Отправка всем пользователям чата, кроме отправителя (всего один получатель)
        continue

      # Если получатель онлайн (есть в группе), в его консьюмер прилетает event с chat_id и text, потом отправляется по сокету на frontend
      # но если пользователь оффлайн, то ничего не происходит
      async_to_sync(self.channel_layer.group_send)(
        str(participant.id),
        {
          'type': 'chat_message',
          'chat_id': chat.id,
          'text': text
        }
      )

    # Ответ после отправки сообщения. Таким образом ты можешь сделать иконку у сообщения "отправка", а когда получишь "ok", можешь поставить иконку "отправлено"
    self.send_json({'status': 'ok', 'chat_id': chat.id})

  def chat_message(self, event: Dict) -> None:
    ''' Если в консьюмер прилетает событие из другого консьюмера, то вызывается эта функция
        Сообщение отправляется по сокету на frontend '''

    self.send_json({'event': 'new_message', **event})
