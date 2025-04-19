# frontend/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Category, Product
from orders.models import Order, OrderItem
from users.models import User
import requests
import json

def home_view(request):
    categories = Category.objects.all()[:4]  # Limit to 4 categories
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:6]  # Latest 6 products
    
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'frontend/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('frontend:home')
        else:
            return render(request, 'frontend/login.html', {'error': 'Invalid username or password'})
    
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
        
        # Basic validation
        if not (username and email and password and first_name and last_name and user_type and phone_number and address):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'frontend/register.html', {'error': 'Please fill in all required fields.'})
        
        if user_type == 'FARMER' and not (farm_name and farm_location):
            messages.error(request, 'Farm name and location are required for farmers.')
            return render(request, 'frontend/register.html', {'error': 'Farm name and location are required for farmers.'})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'frontend/register.html', {'error': 'Username already exists.'})
        
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
                farm_location=farm_location
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to AgroConnect.')
            return redirect('frontend:home')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'frontend/register.html', {'error': f'Error creating account: {str(e)}'})
    
    # For GET request
    user_type = request.GET.get('user_type', 'BUYER')  # Default to BUYER
    return render(request, 'frontend/register.html', {'user_type': user_type})

# In your views.py
def products_view(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    
    # Get category name for display
    category_name = "All"
    if category_id:
        products = products.filter(category_id=category_id)
        try:
            category = Category.objects.get(id=category_id)
            category_name = category.name
        except Category.DoesNotExist:
            pass
    
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    context = {
        'categories': categories,
        'products': products,
        'selected_category': int(category_id) if category_id else None,
        'selected_category_name': category_name,  # Add this line
        'search_query': search_query
    }
    return render(request, 'frontend/products.html', context)



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
        
        if not delivery_address or not contact_phone:
            messages.error(request, 'Delivery address and contact phone are required.')
            return render(request, 'frontend/checkout.html', {'cart': cart})
        
        # Update cart and change status to ORDERED
        cart.delivery_address = delivery_address
        cart.contact_phone = contact_phone
        cart.status = Order.OrderStatus.ORDERED
        cart.save()
        
        # For simplicity, mark the order as paid immediately
        cart.is_paid = True
        cart.save()
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('frontend:order_confirmation', order_id=cart.id)
    
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

@login_required
def order_detail_view(request, order_id):
    if request.user.is_farmer():
        # Farmers can see orders that contain their products
        order = get_object_or_404(Order, id=order_id, items__product__farmer=request.user)
    else:
        # Buyers can see their own orders
        order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    context = {
        'order': order
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
        
        # Handle profile image if uploaded
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()
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

@login_required
def product_form_view(request, product_id=None):
    if not request.user.is_farmer():
        messages.error(request, 'You need to be a farmer to access this page.')
        return redirect('frontend:home')
    
    # For editing an existing product
    product = None
    if product_id:
        product = get_object_or_404(Product, id=product_id, farmer=request.user)
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity_available = request.POST.get('quantity_available')
        unit = request.POST.get('unit')
        is_available = request.POST.get('is_available') == 'on'
        
        # Validate form data
        if not (name and category_id and price and quantity_available and unit):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'frontend/product_form.html', {
                'product': product,
                'categories': categories,
                'error': 'Please fill in all required fields.'
            })
        
        try:
            category = Category.objects.get(id=category_id)
            
            if product:  # Update existing product
                product.name = name
                product.category = category
                product.description = description
                product.price = price
                product.quantity_available = quantity_available
                product.unit = unit
                product.is_available = is_available
            else:  # Create new product
                product = Product(
                    name=name,
                    farmer=request.user,
                    category=category,
                    description=description,
                    price=price,
                    quantity_available=quantity_available,
                    unit=unit,
                    is_available=is_available
                )
            
            # Handle product image if uploaded
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            
            messages.success(request, f'Product {"updated" if product_id else "created"} successfully!')
            return redirect('frontend:farmer_dashboard')
        except Exception as e:
            messages.error(request, f'Error saving product: {str(e)}')
    
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