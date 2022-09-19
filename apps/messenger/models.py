from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Chat(models.Model):
  participants = models.ManyToManyField(
    User,
    related_name='chats',
    verbose_name='katılımcılar'
  )

  class Meta:
    verbose_name = 'sohbet'
    verbose_name_plural = 'sohbetler'

  @property
  def last_message(self) -> models.Model:
    return self.messages.last()

  @property
  def unseen(self) -> int :
    return self.messages.filter(seen=False).count()

  def participants_list(self) -> str:
    return ' – '.join(map(lambda user: user.email, self.participants.all())) or 'Katılımcı yok'

  def __str__(self) -> str:
    return self.participants_list()


class Message(models.Model):
  sender = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='messages',
    verbose_name='gönderici'
  )

  chat = models.ForeignKey(
    Chat,
    on_delete=models.CASCADE,
    related_name='messages',
    verbose_name='sohbet'
  )

  text = models.CharField('mesaj', max_length=1000)
  sent_datetime = models.DateTimeField('ne zaman gonderildi?',auto_now=True)
  seen = models.BooleanField('okundumu?',default=False)

  @property
  def sent_datetime_str(self):
    now = datetime.now()
    sent = self.sent_datetime
    show_month = now.month != sent.month   
    show_year = now.year != sent.year
    return self.sent_datetime.strftime(f'%H:%M{", %b" if show_month else ""}{" %Y" if show_year else ""}')

  class Meta:
    verbose_name = 'mesaj'
    verbose_name_plural = 'mesajlar'

  def __str__(self) -> str:
    return self.text
