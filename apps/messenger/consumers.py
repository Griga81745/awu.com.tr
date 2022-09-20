import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from . import models

User = get_user_model

class ChatConsumer(WebsocketConsumer):
    
    chat_group_prefix = lambda chat_id : f'chat_{chat_id}'

    def connect(self):

        self.user = self.scope['user'] 
        self.peer = User.objects.filter(id=self.scope['url_route']['kwargs']['peer_id']).first()

        if (
            not self.user.is_authenticated or
            not self.peer or
            self.user == self.peer
        ):
            self.close()

        self.chat = models.Chat.objects\
            .filter(participants__in=[self.user])\
            .filter(participants__in=[self.peer])\
            .first()
        
        self.chat_id = self.chat.id

        self.chat.messages.filter(sender=self.peer).update(seen=True)

        for chat in self.user.chats.all():

            async_to_sync(self.channel_layer.group_add)(
                self.chat_group_prefix(chat.id),
                self.channel_name
            )

            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_prefix(self.chat_id),
                {
                    'type': 'peer_online',
                    'peer_id': self.user.id,
                    'status': True
                }
            )

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_send)(
            str(self.chat_id),
            {
                'type': 'peer_online',
                'peer_id': self.user.id,
                'status': False
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_prefix(self.chat_id),
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        message = models.Message.objects.create(
            chat=self.chat,
            sender=self.user,
            text=message_text
        )

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_prefix(self.chat_id),
            {
                'type': 'new_message',
                'message': message_text,
                'peer_id': self.user.id,
                'sent_datetime': message.sent_datetime_str
            }
        )

    def new_message(self, event):

        self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': event['message'],
            'peer_id': event['peer_id'],
            'sent_datetime': event['sent_datetime']
        }))

    def peer_online(self, event):

        if event['peer_id'] == self.user.id : return

        self.send(text_data=json.dumps({
            'type': 'peer_online',
            'peer_id': event['peer_id'],
            'status': event['status'],
        }))