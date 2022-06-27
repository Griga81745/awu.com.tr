from . import models
from django.contrib import admin


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
  list_display = ('last_message', 'participants_list')


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
  list_display = ('chat', 'text')
  search_fields = ('text',)
