# Update users/models.py to add email verification field

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

    # Payment information
    bank_name = models.CharField(max_length=50, blank=True, null=True)  # e.g., MBank, Optima
    bank_account = models.CharField(max_length=50, blank=True, null=True)  # Account number
    bank_qr_code = models.ImageField(upload_to='payment_qr_codes/', blank=True, null=True)  # Uploaded QR code
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    
    def is_farmer(self):
        return self.user_type == self.UserType.FARMER
    
    def is_buyer(self):
        return self.user_type == self.UserType.BUYER
    
    def __str__(self):
        return self.username