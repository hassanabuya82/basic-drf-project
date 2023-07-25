from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser as User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email","first_name","last_name"]
