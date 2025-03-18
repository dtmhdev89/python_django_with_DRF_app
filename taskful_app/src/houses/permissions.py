from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


class IsHouseManagerOrNone(permissions.BasePermission):
    """
    Custom permissions for House Managers to allow only specific privilleges for editting specific house attributes
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        try:
            user_profile = request.user.profile
        except ObjectDoesNotExist:
            user_profile = None
            
        return obj.manager == user_profile
