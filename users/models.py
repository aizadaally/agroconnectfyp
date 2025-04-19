# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class UserType(models.TextChoices):
        FARMER = 'FARMER', _('Farmer')
        BUYER = 'BUYER', _('Buyer')
    
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.BUYER,
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    # For farmers
    farm_name = models.CharField(max_length=255, blank=True, null=True)
    farm_location = models.CharField(max_length=255, blank=True, null=True)
    
    def is_farmer(self):
        return self.user_type == self.UserType.FARMER
    
    def is_buyer(self):
        return self.user_type == self.UserType.BUYER
    
    def __str__(self):
        return self.username