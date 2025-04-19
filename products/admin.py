# products/admin.py

from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'price', 'quantity_available', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description', 'farmer__username')
    readonly_fields = ('created_at', 'updated_at')