# Update products/admin.py to support multilingual fields

from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'name_ru', 'name_ky')
    search_fields = ('name', 'name_en', 'name_ru', 'name_ky')
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Translations', {
            'fields': ('name_en', 'name_ru', 'name_ky'),
            'classes': ('collapse',),
        }),
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'price', 'quantity_available', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'name_en', 'name_ru', 'name_ky', 'description', 'farmer__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('farmer', 'category', 'price', 'quantity_available', 'unit', 'is_available', 'image')
        }),
        ('Default Content', {
            'fields': ('name', 'description'),
        }),
        ('English Translation', {
            'fields': ('name_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Russian Translation', {
            'fields': ('name_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        ('Kyrgyz Translation', {
            'fields': ('name_ky', 'description_ky'),
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)