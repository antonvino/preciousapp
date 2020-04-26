from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.author == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or view it.
    """

    def has_object_permission(self, request, view, obj):
        # Any permissions are only allowed to the owner of the object.
        return obj.author == request.user


class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow users see their profile.
    """

    def has_object_permission(self, request, view, obj):
        # Any permissions are only allowed to the user himself.
        return obj.id == request.user.id