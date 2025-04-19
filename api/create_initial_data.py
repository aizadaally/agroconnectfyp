# api/create_initial_data.py

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agroconnect_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product

User = get_user_model()

def create_initial_data():
    print("Creating initial data...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        print("Admin user created.")
    
    # Create test farmer
    if not User.objects.filter(username='farmer1').exists():
        farmer = User.objects.create_user(
            username='farmer1',
            email='farmer1@example.com',
            password='farmerpass123',
            first_name='John',
            last_name='Farmer',
            user_type='FARMER',
            phone_number='+123456789',
            address='123 Farm Road',
            farm_name='Green Valley Farm',
            farm_location='Central Region'
        )
        print("Test farmer created.")
    
    # Create test buyer
    if not User.objects.filter(username='buyer1').exists():
        buyer = User.objects.create_user(
            username='buyer1',
            email='buyer1@example.com',
            password='buyerpass123',
            first_name='Sarah',
            last_name='Buyer',
            user_type='BUYER',
            phone_number='+987654321',
            address='456 Market Street'
        )
        print("Test buyer created.")
    
    # Create categories
    categories = ['Vegetables', 'Fruits', 'Dairy', 'Grains']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name)
    print("Categories created.")
    
    # Create sample products for the farmer
    vegetable_category = Category.objects.get(name='Vegetables')
    farmer = User.objects.get(username='farmer1')
    
    # Sample vegetable products
    vegetables = [
        {
            'name': 'Tomato',
            'description': 'Fresh, organic tomatoes',
            'price': 2.50,
            'quantity_available': 100,
            'unit': 'kg'
        },
        {
            'name': 'Potato',
            'description': 'High-quality potatoes',
            'price': 1.50,
            'quantity_available': 200,
            'unit': 'kg'
        },
        {
            'name': 'Cabbage',
            'description': 'Large, fresh cabbages',
            'price': 3.00,
            'quantity_available': 50,
            'unit': 'piece'
        }
    ]
    
    for veg in vegetables:
        Product.objects.get_or_create(
            name=veg['name'],
            farmer=farmer,
            category=vegetable_category,
            defaults={
                'description': veg['description'],
                'price': veg['price'],
                'quantity_available': veg['quantity_available'],
                'unit': veg['unit']
            }
        )
    
    print("Sample products created.")
    print("Initial data creation complete.")

if __name__ == '__main__':
    create_initial_data()