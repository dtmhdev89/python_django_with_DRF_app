from rest_framework import permissions


class IsAllowdToEditTaskListOrNone(permissions.BasePermission):
    """
    Custom permissions for TaskListViewSet to only allow creator editing permission.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        user_profile = request.user.profile

        return user_profile == obj.created_by
