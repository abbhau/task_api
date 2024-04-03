from rest_framework.permissions import BasePermission

class CustomUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user.email)
        print(obj.email)
        return bool(request.user.email == obj.email)


class CustomTaskCreate(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role != "developer" )
    

class CustomTaskDelete(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "manager" )
    

