from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class ClientPermissionOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        return bool(
            request.method in self.SAFE_METHODS or
            request.user.client_user and
            request.user.is_authenticated
        )


class ClientPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user.is_client and request.user.is_authenticated)
