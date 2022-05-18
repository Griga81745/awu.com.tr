from .manager import UserManager

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(r'^(0|90)(\d{10})$')


class User(AbstractUser):
  username = None
  email = models.EmailField('Email', unique=True)
  phone_number = models.CharField('Phone Number', max_length=12, validators=[phone_number_validator])
  whatsapp = models.CharField('Whatsapp Number', max_length=12, validators=[phone_number_validator], blank=True)

  is_lawyer = models.BooleanField('Lawyer?', default=False)
  free_consultacy = models.BooleanField('Free?', default=False)
  license_date = models.DateTimeField('License Date', blank=True, null=True)

  city = models.CharField('City', max_length=15, blank=True, null=True)
  website = models.URLField('Website URL', blank=True, null=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  objects = UserManager()

  def __str__(self) -> None:
    return self.email
