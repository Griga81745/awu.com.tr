from . import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
  ordering = ('email',)
  search_fields = ('email',)
  list_display = ('email', 'is_staff', 'is_active')
  list_filter = ('is_staff', 'is_active')

  fieldsets = (
    ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'whatsapp', 'city', 'website')}),
    ('Additional Info', {'fields': ('is_lawyer', 'free_consultacy', 'license_date', 'last_login', 'date_joined')}),
    ('Staff Info', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups'), 'classes': ('collapse',)})
  )

  add_fieldsets = (
    (None, {
      'classes': 'wide',
      'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
    }),
  )
