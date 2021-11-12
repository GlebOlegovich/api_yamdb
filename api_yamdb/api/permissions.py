from rest_framework import permissions, status

ADMIN = 'admin'
MODERATOR = 'moderator'


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        safe = request.method in permissions.SAFE_METHODS
        if request.user.is_authenticated:
            admin_or_superuser = (
                request.user.role == ADMIN
                or request.user.is_superuser
            )
            return safe or admin_or_superuser
        return safe


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"


class AdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Вот пример
            return request.user._is_admin_or_superuser
        return False


class IsUserAnonModerAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            if request.user == obj.author:
                return True, status.HTTP_403_FORBIDDEN
            if (
                request.user.role == ADMIN
                or request.user.role == MODERATOR
                or request.user.is_superuser
            ):
                return (True, status.HTTP_204_NO_CONTENT)
        safe = request.method in permissions.SAFE_METHODS
        if request.user.is_authenticated:
            admin_or_author = (
                request.user.role == 'admin'
                or request.user == obj.author
                or request.user.is_superuser
            )
            return safe or admin_or_author
        return safe
