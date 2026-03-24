from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderModel(admin.ModelAdmin):
    fields = ['user', 'total_price']
    list_filter = []
    list_display = ['id', 'user', 'total_price', 'created_at']
    search_fields = ['user']
