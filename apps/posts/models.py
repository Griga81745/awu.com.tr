from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.users.models import Area

User = get_user_model()

# менеджер для получения опубликованных постов
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(published=True)


class Post(models.Model):
  title = models.CharField('başlık', max_length=30)
  slug = AutoSlugField(verbose_name='slug', populate_from='title', unique=True)
  content = models.TextField('Content')
  published = models.BooleanField('yayınlama tarihi', default=False)
  tags = models.ManyToManyField(Area, verbose_name='ilgili alanlar')

  image = models.ImageField(upload_to='posts/images', default='posts/images/default.jpg', verbose_name='görsel')

  creation_date = models.DateTimeField('yazı tarihi', auto_now_add=True)

  objects = models.Manager()
  published_posts = PublishedManager()

  class Meta:
    verbose_name = 'haber'
    verbose_name_plural = 'haberler'

  def get_absolute_url(self):
    return reverse('blog:post-detail',
      args= [ self.slug ]
    )

  def __str__(self) -> str:
    return self.title


class Comment(models.Model):

  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name='comment',
    related_name='comments'
  )

  post = models.ForeignKey(
    Post,
    on_delete=models.CASCADE,
    verbose_name='post',
    related_name='comments'
  )

  content = models.TextField('content')
  creation_date = models.DateTimeField('tarih', auto_now_add=True)

  MAX_LENGTH = 200

  class Meta:
    verbose_name = 'yorum'
    verbose_name_plural = 'yorumlar'

  def __str__(self) -> str:
    return f'{self.user} - {self.post}'
