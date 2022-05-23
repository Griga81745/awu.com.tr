from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
  title = models.CharField('Title', max_length=30)
  slug = AutoSlugField(verbose_name='Slug', populate_from='title', unique=True)
  content = models.TextField('Content')
  published = models.BooleanField('Published', default=False)

  creation_date = models.DateTimeField('Creation Date', auto_now_add=True)

  def __str__(self) -> str:
    return self.title


class Comment(models.Model):

  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name='Comment',
    related_name='comments'
  )

  post = models.ForeignKey(
    Post,
    on_delete=models.CASCADE,
    verbose_name='Post',
    related_name='comments'
  )

  content = models.TextField('Content')
  creation_date = models.DateTimeField('Creation Date', auto_now_add=True)

  def __str__(self) -> str:
    return f'{self.user} - {self.post}'
