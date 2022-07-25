from django.contrib import admin

from . import models

@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
  search_fields = ('title', 'content')
  list_display = ('title',)
  list_filter = ('id',)

@admin.register(models.Media)
class FAQAdmin(admin.ModelAdmin):
  search_fields = ('title', 'link')
  list_display = ('title',)
  list_filter = ('id',)

