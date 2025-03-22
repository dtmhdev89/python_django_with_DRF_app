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


class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    """
    Custom permissions for TaskViewSet to only allow members of a house access to its task
    """

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.house is not None

        return False

    def has_object_permission(self, request, view, obj):
        user_house = request.user.profile.house
        obj_house = obj.task_list.house

        return user_house == obj_house


class IsAllowdToEditAttachmentElseNone(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.house is not None

        return False
    
    def has_object_permission(self, request, view, obj):
        user_house = request.user.profile.house
        obj_house = obj.task.task_list.house

        return user_house == obj_house
