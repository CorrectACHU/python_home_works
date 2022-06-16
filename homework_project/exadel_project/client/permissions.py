from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsClientProfileOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and hasattr(request.user, "client")
                and request.user.id == request.parser_context['kwargs']['pk']
        )


class IsClientOrReadOnly(permissions.BasePermission):
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


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif hasattr(request.user, "client"):
            return obj.client_owner.profile.id == request.user.id
        return False
