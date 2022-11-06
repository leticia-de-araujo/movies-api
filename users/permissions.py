from rest_framework import permissions
from rest_framework.views import Request, View

from .models import User


class isAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_superuser


class isAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):

        return (
            request.user.is_authenticated
            and request.user == user
            or request.user.is_authenticated
            and request.user.is_superuser
        )
