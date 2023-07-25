from rest_framework.permissions import BasePermission

class CustomPermission(BasePermission):
    def __init__(self, permission):
        self.permission = permission

    def has_permission(self, request, view):
        # Get the user object from the request
        user = request.user

        # Check if the user has the required permission
        return user.has_perm(self.permission)
