from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user.is_superuser is True:
            return True
        return request.user == obj.creator
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser is True:
            return True
        return request.user == obj.user