from django.contrib import admin
from django.conf import settings

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    fields = ['user', 'slug', 'available', 'created', 'updated']
    list_display = ['user', 'slug']
    prepopulated_fields = {'slug': ('user',)}
    list_filter = ['available', 'created', 'updated']
