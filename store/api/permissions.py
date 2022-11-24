from rest_framework import permissions


class IsVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_verified:
            return True 
        return False 
    
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
