from rest_framework import permissions

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    """
    Custom permission for UserViewSet to allow only the owner of a user to edit user's profile.
    Otherwise, allow GET and POST requests.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        print(f"request.user: {request.user}")
        print(f"obj: {obj}")
        if not request.user.is_anonymous:
            return obj == request.user

        return False
