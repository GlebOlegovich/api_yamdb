from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()

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
                if request.user.role == 'admin' or request.user.role == 'moderator':
                    return True
                return False
            return False
        return False