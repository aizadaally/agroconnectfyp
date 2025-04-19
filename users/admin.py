# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 'profile_image', 'farm_name', 'farm_location')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 'profile_image', 'farm_name', 'farm_location')}),
    )
    list_filter = UserAdmin.list_filter + ('user_type',)

admin.site.register(User, CustomUserAdmin)