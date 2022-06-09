from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class ClientProfileOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and hasattr(request.user, "client")
                and request.user.id == request.parser_context['kwargs']['pk']
        )


class ClientOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            hasattr(request.user, "client")
            and request.user.client.is_client
        )


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, "client") and
            request.user.client.is_client
        )