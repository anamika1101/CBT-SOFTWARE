from django.contrib import admin
from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('email', 'name')
