# frontend/urls.py

from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    # Main pages
    path('', views.home_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('products/<int:product_id>/', views.product_detail_view, name='product_detail'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # User profile
    path('profile/', views.profile_view, name='profile'),
    
    # Cart and orders
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:order_id>/confirmation/', views.order_confirmation_view, name='order_confirmation'),
    
    # Farmer pages
    path('farmer/dashboard/', views.farmer_dashboard_view, name='farmer_dashboard'),
    path('farmer/products/add/', views.product_form_view, name='add_product'),
    path('farmer/products/<int:product_id>/edit/', views.product_form_view, name='edit_product'),
    path('farmer/products/<int:product_id>/delete/', views.delete_product_view, name='delete_product'),
]