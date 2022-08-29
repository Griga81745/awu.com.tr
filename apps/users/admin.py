from . import models

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
  ordering = ('email',)
  search_fields = ('email',)
  list_display = ('email', 'is_staff', 'is_active','is_lawyer')
  list_filter = ('is_staff', 'is_active','is_lawyer')

  fieldsets = (
    ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'whatsapp', 'city', 'website','avatar')}),
    ('Additional Info', {'fields': ('is_lawyer', 'consultacy_free', 'consultacy_price', 'license_date', 'last_login', 'date_joined', 'rate', 'areas')}),
    ('Store', {'fields': ('favorites',)}),
    ('Staff Info', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups'), 'classes': ('collapse',)}),
  )

  readonly_fields = (*BaseUserAdmin.readonly_fields, 'rate')

  add_fieldsets = (
    (None, {
      'classes': 'wide',
      'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
    }),
  )


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
  search_fields = ('content',)
  list_display = ('owner', 'destination', 'rate')
  list_filter = ('rate', 'creation_date')

  fieldsets = (
    (None, {'fields': ('owner', 'destination', 'content', 'rate', 'creation_date')}),
  )

  readonly_fields = ('creation_date',)

@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
  search_fields = ('name',)
  list_display = ('name',)