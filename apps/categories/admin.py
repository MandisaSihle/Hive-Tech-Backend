from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryModel(admin.ModelAdmin):
    fields = ["name", "image"]
    list_filter = []
    list_display = ["name", "image"]
    search_fields = ["name"]
