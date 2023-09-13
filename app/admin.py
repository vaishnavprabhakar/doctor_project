from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','username', 'email','is_doctor','is_active', 'is_superuser']
    list_display_links = ['email','first_name', 'last_name','username',]
    ordering = ['id']
    