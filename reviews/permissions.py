from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Review


class IsAdminOrCriticOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method == "GET"
            or request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_critic
        )


class IsAdminOrReviewCriticOrReadOnly(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, review: Review
    ) -> bool:
        return (
            request.method == "GET"
            or request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_critic
            and request.user == review.user
        )
