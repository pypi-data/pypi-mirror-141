from django.contrib import admin
from .models import User


class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone_number', 'is_superuser']
    list_filter = ['username', 'email', 'phone_number']
    search_fields = ['username', 'email', 'phone_number']
    list_display_links = ['id', 'username']


admin.site.register(User, AdminUser)
