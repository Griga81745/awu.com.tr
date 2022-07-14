from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager

User = get_user_model()

# менеджер для получения опубликованных постов
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(published=True)


class Post(models.Model):
  title = models.CharField('Title', max_length=30)
  slug = AutoSlugField(verbose_name='Slug', populate_from='title', unique=True)
  content = models.TextField('Content')
  published = models.BooleanField('Published', default=False)

  image = models.ImageField(upload_to='posts/images',default='posts/images/default.jpg')

  creation_date = models.DateTimeField('Creation Date', auto_now_add=True)

  objects = models.Manager()
  published_posts = PublishedManager()
  tags = TaggableManager()

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
