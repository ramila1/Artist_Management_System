from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsArtist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_artist


class IsAdminOrArtist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_artist)
