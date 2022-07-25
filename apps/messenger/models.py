from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
  participants = models.ManyToManyField(
    User,
    related_name='chats',
    verbose_name='Chats'
  )

  class Meta:
    verbose_name = 'Sohbet'
    verbose_name_plural = 'Sohbetler'

  def last_message(self) -> models.Model:
    return self.messages.last()

  def participants_list(self) -> str:
    return ' – '.join(map(lambda user: user.email, self.participants.all())) or 'No participants'

  def __str__(self) -> str:
    return self.participants_list()


class Message(models.Model):
  sender = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='messages',
    verbose_name='Sender'
  )

  chat = models.ForeignKey(
    Chat,
    on_delete=models.CASCADE,
    related_name='messages',
    verbose_name='Chat'
  )

  text = models.CharField('Text', max_length=1000)

  class Meta:
    verbose_name = 'Mesaj'
    verbose_name_plural = 'Mesajlar'

  def __str__(self) -> str:
    return self.text
