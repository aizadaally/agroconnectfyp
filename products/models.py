# products/models.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_ky = models.CharField(max_length=100, blank=True, null=True)


    def get_translated_name(self):
        """Returns the category name in the current language"""
        from django.utils.translation import get_language
        current_lang = get_language()
        
        if current_lang == 'ru' and self.name_ru:
            return self.name_ru
        elif current_lang == 'ky' and self.name_ky:
            return self.name_ky
        elif current_lang == 'en' and self.name_en:
            return self.name_en
        else:
            return self.name
    
    def __str__(self):
        return self.get_translated_name()
    


    class Meta:
        verbose_name_plural = 'Categories'


        

class Product(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_ky = models.CharField(max_length=200, blank=True, null=True)
    
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    description = models.TextField(blank=True)
    description_en = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    description_ky = models.TextField(blank=True, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50, default='kg')  # kg, piece, bunch, etc.
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_translated_name(self):
        """Returns the product name in the current language"""
        from django.utils.translation import get_language
        current_lang = get_language()
        
        if current_lang == 'ru' and self.name_ru:
            return self.name_ru
        elif current_lang == 'ky' and self.name_ky:
            return self.name_ky
        elif current_lang == 'en' and self.name_en:
            return self.name_en
        else:
            return self.name
    
    def get_translated_description(self):
        """Returns the product description in the current language"""
        from django.utils.translation import get_language
        current_lang = get_language()
        
        if current_lang == 'ru' and self.description_ru:
            return self.description_ru
        elif current_lang == 'ky' and self.description_ky:
            return self.description_ky
        elif current_lang == 'en' and self.description_en:
            return self.description_en
        else:
            return self.description
    
    def __str__(self):
        return self.get_translated_name()