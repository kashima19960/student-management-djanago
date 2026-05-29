"""API permission classes."""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow full access to admin group, read-only for others."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.groups.filter(name="admin").exists()
        )
