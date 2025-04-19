# Create a new file: orders/payment.py

import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from decimal import Decimal

def generate_payment_qr(order_id, amount, recipient_account, bank_name):
    """Generate QR code with payment details"""
    # Format: bank_name://pay?account=XXXX&amount=YYY.YY&reference=ORDER_ID
    payment_data = f"{bank_name.lower()}://pay?account={recipient_account}&amount={amount}&reference=ORDER_{order_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(payment_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to file-like object
    buffer = BytesIO()
    img.save(buffer)
    return buffer.getvalue()

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        FAILED = 'FAILED', 'Failed'
    
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # For tracking
    qr_code = models.ImageField(upload_to='payment_qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmation_code = models.CharField(max_length=8, blank=True, null=True)  # For manual verification
    
    def save(self, *args, **kwargs):
        # Generate a confirmation code if none exists
        if not self.confirmation_code:
            import random
            import string
            self.confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - {self.get_status_display()}"