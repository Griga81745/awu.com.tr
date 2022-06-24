from jinja2 import Environment
from django.middleware.csrf import get_token
from django.urls import reverse
from django.templatetags.static import static

def environment(**options):
	env = Environment(**options)
	env.globals.update({
		"static": static,
		"url": reverse
	})
	return env