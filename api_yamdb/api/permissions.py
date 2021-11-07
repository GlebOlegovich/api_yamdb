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

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST' or request.method == 'DELETE':
            return obj.author == request.user
        if request.method == 'PATCH':
            if obj.author == request.user:
                return True
            if request.user.is_authenticated:
                if (
                    request.user.role == 'admin'
                    or request.user.role == 'moderator'
                ):
                    return True
                return False
            return False
        return False
