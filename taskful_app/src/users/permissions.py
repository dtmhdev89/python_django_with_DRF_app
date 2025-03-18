from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    """
    Custom permission for UserViewSet to allow only the owner of a user to edit user's info.
    Otherwise, allow GET and POST requests.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous:
            return obj == request.user

        return False


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for ProfileViewSet to allow only the owner of a profile to edit owner's profile.
    Otherwise, readonly
    """

    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            try:
                user_profile = request.user.profile
            except ObjectDoesNotExist:
                user_profile = None
            
            return (user_profile is not None
                       and obj == user_profile)
        
        return False

