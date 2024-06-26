from rest_framework import permissions


class StaffOrAuthorOrReadOnly(permissions.BasePermission):
    """Проверка прав доступа для админа, автора или только для чтения."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_staff or obj.user == request.user)
        )
