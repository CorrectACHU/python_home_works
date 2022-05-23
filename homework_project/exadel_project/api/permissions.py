from rest_framework import permissions


class ClientPermissionOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return bool(True)
        elif request.user.is_authenticated:
            return bool(
                request.user.profile.is_client
            )
        else:
            return bool(False)


class ClientPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user.profile.is_client and request.user.is_authenticated)
