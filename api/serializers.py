# api/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.models import Category, Product
from orders.models import Order, OrderItem

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 
                  'user_type', 'phone_number', 'address', 'profile_image',
                  'farm_name', 'farm_location')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # This hashes the password properly
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    farmer_name = serializers.SerializerMethodField()
    farmer_phone = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'farmer', 'farmer_name', 'farmer_phone', 'category', 
                  'category_name', 'description', 'price', 'quantity_available', 'unit',
                  'image', 'is_available', 'created_at', 'updated_at')
        read_only_fields = ('farmer', 'created_at', 'updated_at')
    
    def get_farmer_name(self, obj):
        return obj.farmer.username
    
    def get_farmer_phone(self, obj):
        return obj.farmer.phone_number
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'product_price', 'quantity')
        read_only_fields = ('product_name', 'product_price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_name = serializers.SerializerMethodField()
    buyer_phone = serializers.SerializerMethodField()
    buyer_contact_phone = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'buyer', 'buyer_name', 'buyer_phone', 'buyer_contact_phone',
                  'status', 'created_at', 'updated_at',
                  'delivery_address', 'contact_phone', 'total_amount', 'is_paid', 'items')
        read_only_fields = ('buyer', 'total_amount', 'created_at', 'updated_at')
    
    def get_buyer_name(self, obj):
        return obj.buyer.username
    
    def get_buyer_phone(self, obj):
        return obj.buyer.phone_number
    
    def get_buyer_contact_phone(self, obj):
        return obj.contact_phone