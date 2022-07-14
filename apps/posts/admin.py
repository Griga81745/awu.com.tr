from . import models
from django.contrib import admin


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
  search_fields = ('title', 'content')
  list_display = ('title', 'published', 'creation_date')
  list_filter = ('published', 'creation_date')

  fieldsets = (
    (None, {'fields': ('title', 'content', 'published', 'slug', 'creation_date','tags')}),
  )

  readonly_fields = ('slug', 'creation_date')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
  search_fields = ('content',)
  list_display = ('user', 'post', 'creation_date')
  list_filter = ('creation_date',)

  fieldsets = (
    (None, {'fields': ('user', 'post', 'content', 'creation_date')}),
  )

  readonly_fields = ('creation_date',)
