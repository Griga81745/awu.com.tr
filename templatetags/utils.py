from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def makrdown_format(text):
	return mark_safe(markdown.markdown(text))

@register.simple_tag
def define(val=None):
  return val

@register.filter()
def lookup(value, arg):
    return value.get(arg)