<<<<<<< HEAD
from rest_framework import permissions
from django.contrib.auth import get_user_model

ADMIN = 'admin'
User = get_user_model()
=======
from rest_framework import permissions, status

ADMIN = 'admin'
MODERATOR = 'moderator'


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        safe = request.method in permissions.SAFE_METHODS
        if request.user.is_authenticated:
            return safe or request.user._is_admin
        return safe
>>>>>>> 5cd77ba2e9878adc1972fc6605528422e73bf096


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"


class AdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Вот пример
            return request.user._is_admin
        return False


class IsUserAnonModerAdmin(permissions.BasePermission):
<<<<<<< HEAD

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST' or request.method == 'DELETE':
            return obj.author == request.user
        if request.method == 'PATCH':
            if obj.author == request.user:
                return True
            if request.user.is_authenticated:
                if request.user.role == 'admin' or request.user.role == 'moderator':
                    return True
                return False
            return False
        return False
=======
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            if request.user == obj.author:
                return True, status.HTTP_403_FORBIDDEN
            if request.user._is_moderator:
                return (True, status.HTTP_204_NO_CONTENT)

        safe = request.method in permissions.SAFE_METHODS
        if request.user.is_authenticated:
            admin_or_author = (
                request.user._is_admin
                or request.user == obj.author
            )
            return safe or admin_or_author
        return safe
>>>>>>> 5cd77ba2e9878adc1972fc6605528422e73bf096
