from rest_framework import permissions


class ForeignProfileReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.user != view.get_object()
                and request.method not in permissions.SAFE_METHODS):
            return False
        return True
