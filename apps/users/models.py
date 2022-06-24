from .manager import UserManager
from typing import Tuple, Dict

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from django.core.validators import (
  RegexValidator,
  MinValueValidator,
  MaxValueValidator
)

phone_number_validator = RegexValidator(r'^(0|90)(\d{10})$')


class User(AbstractUser):
  username = None
  email = models.EmailField('Email', unique=True)
  phone_number = models.CharField('Phone Number', max_length=12, blank=True, validators=[phone_number_validator])
  whatsapp = models.CharField('Whatsapp Number', max_length=12, validators=[phone_number_validator], blank=True)

  is_lawyer = models.BooleanField('Is Lawyer?', default=False)
  free_consultacy = models.BooleanField('Free Consultacy?', default=False)
  license_date = models.DateTimeField('License Date', blank=True, null=True)
  rate = models.FloatField('Rate', default=0.0, validators=(MinValueValidator(1), MaxValueValidator(5)))

  city = models.CharField('City', max_length=15, blank=True, null=True)
  website = models.URLField('Website URL', blank=True, null=True)

  avatar = models.ImageField('Avatar',upload_to='users/avatars',default='users/avatars/default.jpg')

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  objects = UserManager()

  def calculate_rate(self) -> None:
    self.rate = self.destination_reviews.all().aggregate(models.Avg('rate'))['rate__avg']
    self.save()

  def __str__(self) -> None:
    return self.email


class RateChoices(models.IntegerChoices):
  bad = 1
  fine = 2
  good = 3
  great = 5


class Review(models.Model):
  owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name='Owner',
    related_name='owner_reviews'
  )

  destination = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name='Destination',
    related_name='destination_reviews'
  )

  content = models.TextField('Content')
  rate = models.IntegerField('Rate', choices=RateChoices.choices, validators=(MinValueValidator(1), MaxValueValidator(5)))

  creation_date = models.DateTimeField('Creation Date', auto_now_add=True)

  def clean(self) -> None:

    if self.owner == self.destination:
      raise ValidationError("User can't review themselves")

    if self.owner.is_lawyer:
      raise ValidationError("Lawyers can't review")

    if not self.destination.is_lawyer:
      raise ValidationError("Only lawyers can't be reviewed")

    return super().clean()

  def save(self, *args: Tuple, **kwargs: Dict) -> None:
    result = super().save(*args, **kwargs)
    self.destination.calculate_rate()
    return result

  def __str__(self) -> str:
    return str(self.owner)
