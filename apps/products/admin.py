from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    fields = ["name", "description", "price", "type", "image", "category"]
    list_filter = []
    list_display = ["name", "description", "price", "type", "image", "category"]
    search_fields = ["name", "description"]