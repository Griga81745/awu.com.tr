from jinja2 import Environment
from django.db.models import Count
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils.html import json_script
from django.templatetags.static import static

from apps.users.models import User, Area
from apps.posts.models import Post
from apps.we.models import Media, SiteSettings

def last_posts(count=5):
	return Post.published_posts.all()[:count]

def most_used_tags(count=0):
	if count:
		return Area.objects.annotate(nused=Count('user')).order_by('-nused')[:count]
	else:
		return Area.objects.annotate(nused=Count('user')).order_by('-nused')[:10]

def get_media():
	return Media.objects.all()

def get_settings():
	return SiteSettings.load()

def environment(**options):
	env = Environment(**options)
	env.globals.update({
		"static": static,
		"url": reverse,
		"last_posts": last_posts,
		"enumerate": enumerate,
		"dir": dir,
		"get_most_used_tags": most_used_tags,
		"get_media": get_media,
		"get_settings": get_settings,
		"json_script": json_script
	})
	return env