import django
from django.contrib import admin

from authentication.models import ActivateToken, ResetToken
from rest_framework.authtoken.models import Token


# Register your models here.


@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ["user","token","created_at","expiry","status"]


@admin.register(ActivateToken  )
class ActivateTokenAdmin(admin.ModelAdmin):
    list_display = ["user","token","created_at","expiry","status"]
