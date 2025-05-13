# orders/models.py

from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CART = 'CART', 'Cart'
        ORDERED = 'ORDERED', 'Order Placed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.CART)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ADD THIS LINE
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.id} - {self.buyer.username} - {self.status}"
    
    def calculate_total(self):
        total = sum(item.subtotal() for item in self.items.all())
        self.total_amount = total
        self.save()
    
    def get_final_total(self):
        """Calculate total including delivery fee"""
        return self.total_amount + self.delivery_fee

# Make sure this method exists in your Order model in orders/models.py

    def mark_as_paid(self):
        """Mark the order as paid and update product quantities"""
        self.is_paid = True
        self.save()
        
        # Update product quantities
        for item in self.items.all():
            if item.product:
                product = item.product
                product.quantity_available -= item.quantity
                if product.quantity_available <= 0:
                    product.is_available = False
                    product.quantity_available = 0  # Ensure it doesn't go negative
                product.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    product_name = models.CharField(max_length=200)  # Store name in case product is deleted
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of order
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
    
    def subtotal(self):
        return self.product_price * self.quantity