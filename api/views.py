# api/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import get_object_or_404
from products.models import Category, Product
from orders.models import Order, OrderItem
from .serializers import (UserSerializer, CategorySerializer, ProductSerializer,
                          OrderSerializer, OrderItemSerializer)
from .permissions import IsFarmerOrReadOnly, IsOwnerOrReadOnly

User = get_user_model()

# Authentication Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            # Automatically log the user in after registration
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser|permissions.IsAuthenticatedOrReadOnly]

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsFarmerOrReadOnly(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_products(self, request):
        products = Product.objects.filter(farmer=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        if category_id:
            products = Product.objects.filter(category_id=category_id, is_available=True)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)

# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.is_farmer():
            # Farmers can see orders containing their products
            return Order.objects.filter(items__product__farmer=user).distinct()
        # Buyers can see their own orders
        return Order.objects.filter(buyer=user)
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def cart(self, request):
        cart, created = Order.objects.get_or_create(
            buyer=request.user,
            status=Order.OrderStatus.CART
        )
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product is available
        if not product.is_available or product.quantity_available < quantity:
            return Response({'error': 'Product not available in requested quantity'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Check if item already exists in order
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                'product_name': product.name,
                'product_price': product.price,
                'quantity': quantity
            }
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        order.calculate_total()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        order = self.get_object()
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response({'error': 'Item ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = OrderItem.objects.get(id=item_id, order=order)
            item.delete()
            order.calculate_total()
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except OrderItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def update_item_quantity(self, request, pk=None):
        order = self.get_object()
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        if not item_id or not quantity:
            return Response({'error': 'Item ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = OrderItem.objects.get(id=item_id, order=order)
            quantity = int(quantity)
            
            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()
            
            order.calculate_total()
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except OrderItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        order = self.get_object()
        
        if order.status != Order.OrderStatus.CART:
            return Response({'error': 'Order is not in cart status'}, status=status.HTTP_400_BAD_REQUEST)
        
        delivery_address = request.data.get('delivery_address')
        contact_phone = request.data.get('contact_phone')
        
        if not delivery_address or not contact_phone:
            return Response({'error': 'Delivery address and contact phone are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        order.delivery_address = delivery_address
        order.contact_phone = contact_phone
        order.status = Order.OrderStatus.ORDERED
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        order = self.get_object()
        
        if order.is_paid:
            return Response({'error': 'Order is already marked as paid'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.is_paid = True
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)