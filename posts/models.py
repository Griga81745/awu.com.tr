from django.db import models
from autoslug import AutoSlugField


class Post(models.Model):
  title = models.CharField('Title', max_length=30)
  slug = AutoSlugField(verbose_name='Slug', populate_from='title', unique=True)
  content = models.TextField('Content')
  published = models.BooleanField('Published', default=False)

  creation_date = models.DateTimeField('Creation Date', auto_now_add=True)

  def __str__(self) -> str:
    return self.title
