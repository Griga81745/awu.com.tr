from . import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
  ordering = ('email',)
  list_display = BaseUserAdmin.list_display[1:]

  fieldsets = (
    ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'whatsapp', 'city', 'website')}),
    ('Additional Info', {'fields': ('is_lawyer', 'free_consultacy', 'license_date', 'last_login', 'date_joined')}),
    ('Staff Info', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups'), 'classes': ('collapse',)})
  )
