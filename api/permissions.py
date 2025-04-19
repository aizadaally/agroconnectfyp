# api/permissions.py

from rest_framework import permissions

class IsFarmerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow farmers to create/edit products.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to farmers
        return request.user.is_authenticated and request.user.is_farmer()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'farmer'):
            return obj.farmer == request.user
        elif hasattr(obj, 'buyer'):
            return obj.buyer == request.user
        return False