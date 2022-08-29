from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class Ticket(models.Model):
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='ticket',
    verbose_name='User',
    unique=True
  )

  ticket = models.CharField('ticket', max_length=32, unique=True, validators=[MinLengthValidator(32)])

  def __str__(self) -> str:
    return str(self.user)
