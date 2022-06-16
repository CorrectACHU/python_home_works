from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class ForUpdateCompanyOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, "company") and obj.profile_id == request.user:
            return True


class IsCompanyOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif hasattr(request.user, "company"):
            return obj.profile_id.id == request.user.id
        return False


class IsCompanyProfileOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, "company") and hasattr(request.user.company, "is_company"):
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if hasattr(request.user, "company") and hasattr(request.user.company, "is_company"):
            return obj.company.profile_id.id == request.user.id
        return False
