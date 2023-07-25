from rest_framework import permissions

class AdministratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT','POST','PATCH']:
            return bool(request.user.is_superuser or request.user.role == 'Administrator')
        return True