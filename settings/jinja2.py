from jinja2 import Environment
from django.middleware.csrf import get_token
from django.urls import reverse
from django.templatetags.static import static

from apps.posts.models import Post

def last_posts(count=5):
	return Post.published_posts.all()[:count]

def most_used_tags(count=0):
	if count:
		return Post.tags.most_common()[:count]
	else:
		return Post.tags.most_common()


def environment(**options):
	env = Environment(**options)
	env.globals.update({
		"static": static,
		"url": reverse,
		"last_posts": last_posts,
		"enumerate": enumerate,
		"dir": dir,
		"get_most_used_tags": most_used_tags
	})
	return env