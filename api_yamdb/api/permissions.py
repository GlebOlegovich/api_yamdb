from rest_framework import permissions

ADMIN = 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == ADMIN))


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"


class AdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == ADMIN
                or request.user.is_superuser
            )
        return False


class IsUserAnonModerAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        safe = request.method in permissions.SAFE_METHODS
        authenticated = request.user.is_authenticated
        if request.user.is_authenticated:
            admin_or_author = (
                request.user.role == 'admin'
                or request.user == obj.author
            )
            return (safe or (authenticated and admin_or_author))
        return safe
