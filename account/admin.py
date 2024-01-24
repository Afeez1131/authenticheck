from django.contrib import admin
from account.models import OneTimeLogin


@admin.register(OneTimeLogin)
class OneTimeLoginAdmin(admin.ModelAdmin):
    list_display = ['user']