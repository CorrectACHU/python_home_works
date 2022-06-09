from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class CompanyProfileOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and hasattr(request.user, "company")
                and request.user.id == request.parser_context['kwargs']['pk']
        )


class CompanyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            hasattr(request.user, "company")
            and request.user.company.is_company
        )
