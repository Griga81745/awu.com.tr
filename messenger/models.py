from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
  users = models.ManyToManyField(
    User,
    related_name='conversations'
  )

  @admin.display(description='Last Message')
  def last_message(self) -> models.Model:
    return self.messages.last() or 'No messages'

  def __str__(self) -> str:
    return f'Conversation {self.id} - {self.last_message()}'

class Message(models.Model):
  conversation = models.ForeignKey(
    Conversation,
    on_delete=models.CASCADE,
    verbose_name='Conversation',
    related_name='messages'
  )

  sender = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name='Sender',
    related_name='messages'
  )

  text = models.CharField('Text', max_length=500)
  creation_date = models.DateTimeField('Creation Date', auto_now_add=True)

  def __str__(self) -> str:
    return f'{self.sender} - {self.conversation.id}'
