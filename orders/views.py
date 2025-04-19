# orders/views.py - Create payment views

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Order
from .payment import Payment, generate_payment_qr
import base64

@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if order.is_paid:
        messages.info(request, "This order has already been paid.")
        return redirect('frontend:order_confirmation', order_id=order.id)
    
    # If payment exists, use it; otherwise create new
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={'amount': order.total_amount}
    )
    
    # Find the farmer(s) for this order
    farmers = {}
    for item in order.items.all():
        if item.product and item.product.farmer:
            farmer = item.product.farmer
            if farmer.id not in farmers:
                farmers[farmer.id] = {
                    'name': farmer.get_full_name() or farmer.username,
                    'bank_name': farmer.bank_name,
                    'bank_account': farmer.bank_account,
                    'qr_code': farmer.bank_qr_code.url if farmer.bank_qr_code else None,
                    'amount': 0,
                    'items': []
                }
            
            # Calculate amount for this farmer
            item_total = item.product_price * item.quantity
            farmers[farmer.id]['amount'] += item_total
            farmers[farmer.id]['items'].append({
                'name': item.product_name,
                'quantity': item.quantity,
                'price': item.product_price,
                'total': item_total
            })
    
    context = {
        'order': order,
        'payment': payment,
        'farmers': farmers.values()
    }
    
    return render(request, 'frontend/payment.html', context)

@login_required
def verify_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')
        
        # Check if payment exists with this confirmation code
        try:
            payment = Payment.objects.get(order=order, confirmation_code=confirmation_code)
            payment.status = Payment.PaymentStatus.CONFIRMED
            payment.save()
            
            # Mark the order as paid
            order.mark_as_paid()
            
            messages.success(request, "Payment verified successfully!")
            return redirect('frontend:order_confirmation', order_id=order.id)
        except Payment.DoesNotExist:
            messages.error(request, "Invalid confirmation code. Please try again.")
    
    return redirect('frontend:payment', order_id=order.id)

@login_required
def manual_payment_confirmation(request, order_id):
    """For farmers to manually confirm they received payment"""
    # Only farmers with products in this order can confirm
    order = get_object_or_404(Order, id=order_id)
    
    # Check if this farmer has products in the order
    if not order.items.filter(product__farmer=request.user).exists():
        messages.error(request, "You don't have any products in this order.")
        return redirect('frontend:farmer_dashboard')
    
    if request.method == 'POST' and not order.is_paid:
        # Mark the order as paid
        order.mark_as_paid()
        messages.success(request, "Payment confirmed successfully!")
        
        # Find or create a payment and mark it as confirmed
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={'amount': order.total_amount}
        )
        payment.status = Payment.PaymentStatus.CONFIRMED
        payment.save()
    
    return redirect('frontend:order_detail', order_id=order.id)