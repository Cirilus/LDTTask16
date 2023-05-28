from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.company:
            return True
