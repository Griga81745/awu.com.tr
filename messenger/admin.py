from . import models
from django.contrib import admin


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
  list_display = ('last_message',)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
  search_fields = ('text',)
  list_display = ('sender', 'conversation', 'creation_date', 'text')
  list_filter = ('creation_date',)

  readonly_fields = ('creation_date',)
