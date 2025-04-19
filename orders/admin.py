# orders/admin.py

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'subtotal')
    
    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Subtotal'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'total_amount', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('buyer__username', 'buyer__email')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]