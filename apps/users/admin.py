from django.contrib import admin
from .models import User


@admin.register(User)
class UserModel(admin.ModelAdmin):
    fields = ['name', 'email', 'password', 'token', 'token_expires']
    list_display = ['name', 'email', 'token']
    search_fields = ['name', 'email']