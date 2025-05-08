# Update frontend/urls.py to add verification endpoints

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
    path('verify-email/<str:token>/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_view, name='resend_verification'),
    
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

    # Payment URLs
    path('orders/<int:order_id>/payment/', views.payment_page, name='payment'),
    path('orders/<int:order_id>/verify-payment/', views.verify_payment, name='verify_payment'),
    path('orders/<int:order_id>/confirm-payment/', views.manual_payment_confirmation, name='confirm_payment'),

    path('test-language/', views.test_language, name='test_language'),

    path('test-email/', views.test_email, name='test_email'),
]