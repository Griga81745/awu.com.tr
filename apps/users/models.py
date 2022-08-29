from .manager import UserManager, LawyerManager
from autoslug import AutoSlugField
from typing import Tuple, Dict

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
)


phone_number_validator = RegexValidator(r'^(0|90)(\d{10})$')


class Area(models.Model):
    name = models.CharField('alan adı', max_length=50)
    slug = AutoSlugField(verbose_name='slug', populate_from='name', primary_key=True)

    class Meta:
        verbose_name = 'alan'
        verbose_name_plural = 'alanlar'

    def get_absolute_url(self):
        return f'{reverse("users:search")}?areas={self.slug}'
    
    def __str__(self):
        return f'{self.name} ({self.user_set.count()})'



class User(AbstractUser):

    LIMIT_FAVORITES = 30
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    email = models.EmailField('e-posta', unique=True)
    phone_number = models.CharField('telefon numarası', max_length=12, blank=True, validators=[phone_number_validator])
    whatsapp = models.CharField('whatsapp numarası', max_length=12, validators=[phone_number_validator], blank=True)

    is_lawyer = models.BooleanField('avukatmıdır?', default=False)
    consultacy_free = models.BooleanField('bedava danışmanlık', default=False)
    consultacy_price = models.PositiveIntegerField('danışmanlık fiyatı', default=0)
    license_date = models.DateTimeField('lisans aldığı tarih', blank=True, null=True)
    rate = models.FloatField('değerlendirme', default=0.0, validators=(MinValueValidator(1), MaxValueValidator(5)))

    city = models.CharField('İlçe', max_length=15, blank=True, null=True)
    website = models.URLField('website adresi', blank=True, null=True)

    avatar = models.ImageField('profil resmi', upload_to='users/avatars', default='users/avatars/default.jpg')
    bio = models.TextField('hakkında')

    areas = models.ManyToManyField(Area, verbose_name='alanlar') 
    favorites = models.ManyToManyField('self', verbose_name='favoriler', limit_choices_to={'is_lawyer':True}, blank=True)

    objects = UserManager()
    lawyers = LawyerManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.title()

    def clean(self, *args, **kwargs):
        if self.favorites.count() > self.LIMIT_FAVORITES:
            raise ValidationError('En fazla 10 favori eklenebilir.')

    def get_absolute_url(self):
        return reverse('users:profile-detail',
            args=[self.id]
        )

    def calculate_rate(self) -> None:
        self.rate = round(self.destination_reviews.all().aggregate(models.Avg('rate'))['rate__avg'], 1)
        self.save()

    def is_favorite(self,user) -> bool :
        return user in self.favorites.all()

    def __str__(self) -> None:
        return f'{self.full_name} -  {self.email}'


class RateChoices(models.IntegerChoices):
    bad = 1
    fine = 2
    good = 3
    great = 5


class Review(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='owner',
        related_name='owner_reviews'
    )

    destination = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Destination',
        related_name='destination_reviews'
    )

    MIN_CONTENT_LENGTH = 20
    MAX_CONTENT_LENGTH = 200

    content = models.TextField('içerik', validators=(
        MinLengthValidator(MIN_CONTENT_LENGTH),
        MaxLengthValidator(MAX_CONTENT_LENGTH)
    ))

    rate = models.IntegerField('puan', choices=RateChoices.choices, validators=(MinValueValidator(1), MaxValueValidator(5)))

    creation_date = models.DateTimeField('tarih', auto_now_add=True)

    class Meta:
        verbose_name = 'eleştiri'
        verbose_name_plural = 'eleştirilerr'

    def save(self, *args: Tuple, **kwargs: Dict) -> None:

        if self.__class__.objects.filter(owner=self.owner, destination=self.destination) and not self.__class__.objects.filter(id=self.id):
            raise ValidationError("İki kere yorum yapamazsınız !")

        if self.owner == self.destination:
            raise ValidationError("Kendinize yorum yapamazsınız !")

        if self.owner.is_lawyer:
            raise ValidationError("Avukatlar yorum yapamazlar !")

        if not self.destination.is_lawyer:
            raise ValidationError("Sadece avukatlar yorum alabilirler !")

        result = super().save(*args, **kwargs)
        self.destination.calculate_rate()
        return result

    def __str__(self) -> str:
        return str(self.owner)
