from rest_framework import permissions


class RolePermission(permissions.BasePermission):
    """Allow access only to users with specific roles."""

    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles