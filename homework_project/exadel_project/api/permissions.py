from rest_framework import permissions


class ClientUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and hasattr(request.user, "client")
                # and request.user.client.is_client
        )

# class ClientPermission(permissions.IsAuthenticated):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             return bool(request.user.profile.is_client and request.user.is_authenticated)
#         return False
