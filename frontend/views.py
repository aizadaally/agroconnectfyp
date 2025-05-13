# frontend/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Category, Product
from orders.models import Order, OrderItem
from users.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
import json
import base64
import qrcode
from io import BytesIO
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.utils.translation import gettext as _
from users.models import User
from users.verification import EmailVerificationToken
from django.db.models import Q
from products.models import Category, Product
from django.utils import timezone  # Add this line
from datetime import timedelta  # Add this line

# Update the products_view function in frontend/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.translation import get_language
from products.models import Category, Product
from django.http import JsonResponse
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def test_email(request):
    """Test view to check if emails are working"""
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)
    
    recipient = request.GET.get('email', request.user.email)
    
    try:
        send_mail(
            subject='Test Email from AgroConnect',
            message='This is a test email from AgroConnect Naryn.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        # Print email configuration for debugging
        config = {
            'EMAIL_BACKEND': settings.EMAIL_BACKEND,
            'EMAIL_HOST': settings.EMAIL_HOST,
            'EMAIL_PORT': settings.EMAIL_PORT,
            'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
            'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
            'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
            'recipient': recipient
        }
        
        return HttpResponse(f"Test email sent to {recipient}! Configuration: {config}")
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return HttpResponse(f"Error sending test email: {str(e)}\n\n{error_details}", status=500)



def test_language(request):
    """View to test language settings"""
    current_language = get_language()
    sample_translations = {
        'home': _('Home'),
        'products': _('Products'),
        'categories': _('Categories'),
        'search': _('Search'),
    }
    
    debug_info = {
        'current_language': current_language,
        'session_language': request.session.get('_language', 'Not set in session'),
        'cookie_language': request.COOKIES.get('django_language', 'Not set in cookie'),
        'translations': sample_translations,
        'session_items': dict(request.session),
    }
    
    return JsonResponse(debug_info)



def products_view(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    
    # Get category name for display
    category_name = _("All")
    if category_id:
        products = products.filter(category_id=category_id)
        try:
            category = Category.objects.get(id=category_id)
            category_name = category.get_translated_name()
        except Category.DoesNotExist:
            pass
    
    # Handle search with multilingual support
    current_lang = get_language()
    
    if search_query:
        # Create different filters based on the current language
        if current_lang == 'ru':
            products = products.filter(
                Q(name_ru__icontains=search_query) | 
                Q(name__icontains=search_query) |
                Q(description_ru__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        elif current_lang == 'ky':
            products = products.filter(
                Q(name_ky__icontains=search_query) | 
                Q(name__icontains=search_query) |
                Q(description_ky__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        elif current_lang == 'en':
            products = products.filter(
                Q(name_en__icontains=search_query) | 
                Q(name__icontains=search_query) |
                Q(description_en__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        else:
            # Default fallback
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
    
    context = {
        'categories': categories,
        'products': products,
        'selected_category': int(category_id) if category_id else None,
        'selected_category_name': category_name,
        'search_query': search_query
    }
    return render(request, 'frontend/products.html', context)




def home_view(request):
    # Get dashboard statistics
    from users.models import User  # Make sure this import is correct
    
    # Count active farmers
    total_farmers = User.objects.filter(user_type='FARMER', is_active=True).count()
    
    # Count available products
    total_products = Product.objects.filter(is_available=True).count()
    
    # Count districts (you might want to add a district model later)
    total_districts = 5  # At-Bashy, Naryn, Ak-Talaa, Jumgal, Kochkor
    
    # Get categories and products for display
    categories = Category.objects.all()[:4]  # Limit to 4 categories
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:6]  # Latest 6 products
    
    context = {
        'categories': categories,
        'products': products,
        'total_farmers': total_farmers,
        'total_products': total_products,
        'total_districts': total_districts,
        'customer_satisfaction': 98,  # This can be calculated from ratings later
    }
    return render(request, 'frontend/home.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if email is verified
            if not user.email_verified:
                messages.warning(request, _('Please verify your email address. Check your inbox or request a new verification email.'))
                return render(request, 'frontend/login.html', {'error': _('Email not verified'), 'unverified_email': user.email})
            
            login(request, user)
            messages.success(request, _('You have successfully logged in!'))
            return redirect('frontend:home')
        else:
            return render(request, 'frontend/login.html', {'error': _('Invalid username or password')})
    
    return render(request, 'frontend/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('frontend:home')

# frontend/views.py (continued)

def register_view(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        farm_name = request.POST.get('farm_name', '')
        farm_location = request.POST.get('farm_location', '')

          # Add debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Registration attempt - Username: {username}, Email: {email}")
        
        # Basic validation
        if not (username and email and password and first_name and last_name and user_type and phone_number and address):
            messages.error(request, _('Please fill in all required fields.'))
            return render(request, 'frontend/register.html', {'error': _('Please fill in all required fields.')})
        
        if user_type == 'FARMER' and not (farm_name and farm_location):
            messages.error(request, _('Farm name and location are required for farmers.'))
            return render(request, 'frontend/register.html', {'error': _('Farm name and location are required for farmers.')})
        
        # Check if username already exists - do a case-insensitive check
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, _('Username already exists. Please choose another one.'))
            return render(request, 'frontend/register.html', {'error': _('Username already exists.')})
        
        # Check if email already exists
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, _('Email already exists. Please use another email.'))
            return render(request, 'frontend/register.html', {'error': _('Email already exists.')})
        
        # Create new user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                phone_number=phone_number,
                address=address,
                farm_name=farm_name,
                farm_location=farm_location,
                email_verified=False  # Initially set to False
            )
            
            # Create and send verification email
            verification_token = EmailVerificationToken.create_verification_token(user)
            verification_token.send_verification_email(request)
            
            # Log the user in
            login(request, user)
            
            messages.success(request, _('Account created successfully! Please check your email to verify your account.'))
            return redirect('frontend:home')
        except Exception as e:
            messages.error(request, _('Error creating account: {error}').format(error=str(e)))
            return render(request, 'frontend/register.html', {'error': _('Error creating account: {error}').format(error=str(e))})
    
    # For GET request
    user_type = request.GET.get('user_type', 'BUYER')  # Default to BUYER
    return render(request, 'frontend/register.html', {'user_type': user_type})




def verify_email_view(request, token):
    """View to handle email verification"""
    verification_token = get_object_or_404(EmailVerificationToken, token=token)
    
    if not verification_token.is_valid():
        messages.error(request, _('Verification link has expired. Please request a new one.'))
        return redirect('frontend:resend_verification')
    
    # Mark user as verified
    user = verification_token.user
    user.email_verified = True
    user.save()
    
    # Delete the token since it's been used
    verification_token.delete()
    
    messages.success(request, _('Email verified successfully! Your account is now fully activated.'))
    return redirect('frontend:profile')

def resend_verification_view(request):
    """View to resend verification email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            if user.email_verified:
                messages.info(request, _('Your email is already verified.'))
                return redirect('frontend:login')
            
            # Create and send new verification email
            verification_token = EmailVerificationToken.create_verification_token(user)
            verification_token.send_verification_email(request)
            
            messages.success(request, _('Verification email has been resent. Please check your inbox.'))
            return redirect('frontend:login')
        except User.DoesNotExist:
            messages.error(request, _('No account found with this email address.'))
    
    return render(request, 'frontend/resend_verification.html')




def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get related products in the same category
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product.id)[:3]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'frontend/product_detail.html', context)

@login_required
def cart_view(request):
    # Get or create a cart for the user
    cart, created = Order.objects.get_or_create(
        buyer=request.user,
        status=Order.OrderStatus.CART
    )
    
    context = {
        'cart': cart
    }
    return render(request, 'frontend/cart.html', context)

# Update the checkout_view function in frontend/views.py

@login_required
def checkout_view(request):
    # Get the user's cart
    try:
        cart = Order.objects.get(buyer=request.user, status=Order.OrderStatus.CART)
        if not cart.items.exists():
            messages.warning(request, 'Your cart is empty.')
            return redirect('frontend:cart')
    except Order.DoesNotExist:
        messages.warning(request, 'Your cart is empty.')
        return redirect('frontend:cart')
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        contact_phone = request.POST.get('contact_phone')
        delivery_area = request.POST.get('delivery_area', 'city')  # Get delivery area
        
        if not delivery_address or not contact_phone:
            messages.error(request, 'Delivery address and contact phone are required.')
            return render(request, 'frontend/checkout.html', {'cart': cart})
        
        # Calculate delivery fee based on area
        delivery_fee = 0
        if delivery_area == 'suburbs':
            delivery_fee = 50
        elif delivery_area == 'villages':
            delivery_fee = 100
        
        # Update cart and change status to ORDERED
        cart.delivery_address = delivery_address
        cart.contact_phone = contact_phone
        cart.delivery_fee = delivery_fee  # Set the delivery fee
        cart.status = Order.OrderStatus.ORDERED
        cart.save()
        
        messages.success(request, 'Your order has been placed! Please complete the payment.')
        return redirect('frontend:payment', order_id=cart.id)
    
    context = {
        'cart': cart
    }
    return render(request, 'frontend/checkout.html', context)

@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if order.status == Order.OrderStatus.CART:
        return redirect('frontend:cart')
    
    context = {
        'order': order
    }
    return render(request, 'frontend/order_confirmation.html', context)

@login_required
def orders_view(request):
    if request.user.is_farmer():
        # Farmers see orders that contain their products
        orders = Order.objects.filter(
            items__product__farmer=request.user, 
            status__in=[Order.OrderStatus.ORDERED, Order.OrderStatus.COMPLETED]
        ).distinct()
    else:
        # Buyers see their orders
        orders = Order.objects.filter(
            buyer=request.user,
            status__in=[Order.OrderStatus.ORDERED, Order.OrderStatus.COMPLETED]
        )
    
    context = {
        'orders': orders
    }
    return render(request, 'frontend/orders.html', context)

# In your order_detail_view function in views.py
@login_required
def order_detail_view(request, order_id):
    if request.user.is_farmer():
        # Farmers can see orders that contain their products
        order = get_object_or_404(Order, id=order_id, items__product__farmer=request.user)
        has_farmer_products = True  # Since we filtered by this in the query
    else:
        # Buyers can see their own orders
        order = get_object_or_404(Order, id=order_id, buyer=request.user)
        has_farmer_products = False
    
    context = {
        'order': order,
        'has_farmer_products': has_farmer_products
    }
    return render(request, 'frontend/order_detail.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Update user profile
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        
        if user.is_farmer():
            user.farm_name = request.POST.get('farm_name')
            user.farm_location = request.POST.get('farm_location')
            request.user.bank_name = request.POST.get('bank_name', '')
            request.user.bank_account = request.POST.get('bank_account', '')
        
        # Handle profile image if uploaded
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        # Handle bank QR code upload
        if 'bank_qr_code' in request.FILES:
                request.user.bank_qr_code = request.FILES['bank_qr_code']
        
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('frontend:profile')
    
    context = {
        'user': request.user
    }
    return render(request, 'frontend/profile.html', context)

@login_required
def farmer_dashboard_view(request):
    if not request.user.is_farmer():
        messages.error(request, 'You need to be a farmer to access this page.')
        return redirect('frontend:home')
    
    # Get farmer's products
    products = Product.objects.filter(farmer=request.user)
    
    # Get orders containing farmer's products
    orders = Order.objects.filter(
        items__product__farmer=request.user,
        status__in=[Order.OrderStatus.ORDERED, Order.OrderStatus.COMPLETED]
    ).distinct()
    
    context = {
        'products': products,
        'orders': orders
    }
    return render(request, 'frontend/farmer_dashboard.html', context)

# Update the product_form_view function in frontend/views.py

@login_required
def product_form_view(request, product_id=None):
    if not request.user.is_farmer():
        messages.error(request, _('You need to be a farmer to access this page.'))
        return redirect('frontend:home')
    
    # For editing an existing product
    product = None
    if product_id:
        product = get_object_or_404(Product, id=product_id, farmer=request.user)
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        # Get basic fields
        name = request.POST.get('name')
        name_en = request.POST.get('name_en')
        name_ru = request.POST.get('name_ru')
        name_ky = request.POST.get('name_ky')
        
        category_id = request.POST.get('category')
        
        description = request.POST.get('description')
        description_en = request.POST.get('description_en')
        description_ru = request.POST.get('description_ru')
        description_ky = request.POST.get('description_ky')
        
        price = request.POST.get('price')
        quantity_available = request.POST.get('quantity_available')
        unit = request.POST.get('unit')
        is_available = request.POST.get('is_available') == 'on'
        
        # Validate form data
        if not (name and category_id and price and quantity_available and unit):
            messages.error(request, _('Please fill in all required fields.'))
            return render(request, 'frontend/product_form.html', {
                'product': product,
                'categories': categories,
                'error': _('Please fill in all required fields.')
            })
        
        try:
            category = Category.objects.get(id=category_id)
            
            if product:  # Update existing product
                product.name = name
                product.name_en = name_en
                product.name_ru = name_ru
                product.name_ky = name_ky
                
                product.category = category
                
                product.description = description
                product.description_en = description_en
                product.description_ru = description_ru
                product.description_ky = description_ky
                
                product.price = price
                product.quantity_available = quantity_available
                product.unit = unit
                product.is_available = is_available
            else:  # Create new product
                product = Product(
                    name=name,
                    name_en=name_en,
                    name_ru=name_ru,
                    name_ky=name_ky,
                    
                    farmer=request.user,
                    category=category,
                    
                    description=description,
                    description_en=description_en,
                    description_ru=description_ru,
                    description_ky=description_ky,
                    
                    price=price,
                    quantity_available=quantity_available,
                    unit=unit,
                    is_available=is_available
                )
            
            # Handle product image if uploaded
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            
            messages.success(request, _('Product {status} successfully!').format(
                status=_("updated") if product_id else _("created")
            ))
            return redirect('frontend:farmer_dashboard')
        except Exception as e:
            messages.error(request, _('Error saving product: {error}').format(error=str(e)))
    
    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'frontend/product_form.html', context)





@login_required
def delete_product_view(request, product_id):
    if not request.user.is_farmer():
        messages.error(request, 'You need to be a farmer to access this page.')
        return redirect('frontend:home')
    
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('frontend:farmer_dashboard')
    
    context = {
        'product': product
    }
    return render(request, 'frontend/delete_product.html', context)


@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if order.is_paid:
        messages.info(request, "This order has already been paid.")
        return redirect('frontend:order_confirmation', order_id=order.id)
    
    # Find the farmer(s) for this order
    farmers = {}
    for item in order.items.all():
        if item.product and item.product.farmer:
            farmer = item.product.farmer
            if farmer.id not in farmers:
                farmers[farmer.id] = {
                    'name': farmer.get_full_name() or farmer.username,
                    'bank_name': getattr(farmer, 'bank_name', ''),
                    'bank_account': getattr(farmer, 'bank_account', ''),
                    'qr_code': farmer.bank_qr_code.url if hasattr(farmer, 'bank_qr_code') and farmer.bank_qr_code else None,
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
    
    # Generate a confirmation code
    import random
    import string
    confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    context = {
        'order': order,
        'farmers': farmers.values(),
        'confirmation_code': confirmation_code,
    }
    
    return render(request, 'frontend/payment.html', context)

# Update the verify_payment function in frontend/views.py

@login_required
def verify_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if order.is_paid:
        messages.info(request, "This order has already been paid.")
        return redirect('frontend:order_confirmation', order_id=order.id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Handle different payment methods
        if payment_method == 'cash':
            # Cash on Delivery - immediately confirm
            order.mark_as_paid()
            messages.success(request, "Order placed successfully! Payment will be collected on delivery.")
            return redirect('frontend:order_confirmation', order_id=order.id)
            
        elif payment_method == 'direct':
            # Direct payment to farmers - check if confirmation checkbox is checked
            direct_confirmation = request.POST.get('direct_confirmation')
            if direct_confirmation:
                order.mark_as_paid()
                messages.success(request, "Payment confirmed successfully!")
                return redirect('frontend:order_confirmation', order_id=order.id)
            else:
                messages.error(request, "Please confirm that you have paid the farmers.")
                
        elif payment_method == 'mobile':
            # Mobile payment - verify transaction ID
            transaction_id = request.POST.get('transaction_id')
            if transaction_id:
                # In a real app, you would verify this with the payment provider
                # For now, we'll just accept any transaction ID
                order.mark_as_paid()
                messages.success(request, "Mobile payment verified successfully!")
                return redirect('frontend:order_confirmation', order_id=order.id)
            else:
                messages.error(request, "Please enter a valid transaction ID.")
        
        elif payment_method == 'bank':
            # Bank transfer - this method would need a confirmation code
            confirmation_code = request.POST.get('confirmation_code')
            if confirmation_code:
                # For demo purposes, accept any code
                order.mark_as_paid()
                messages.success(request, "Bank transfer confirmed successfully!")
                return redirect('frontend:order_confirmation', order_id=order.id)
            else:
                messages.error(request, "Please enter the confirmation code from your bank receipt.")
        
        else:
            messages.error(request, "Invalid payment method selected.")
    
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
    
    return redirect('frontend:order_detail', order_id=order.id)



def debug_image_urls(request):
    products = Product.objects.all()[:5]  # Get first 5 products
    urls = {
        p.name: {
            'image_field': p.image.name if p.image else None,
            'resolved_url': p.image.url if p.image else None,
        } for p in products
    }
    return JsonResponse(urls)   


