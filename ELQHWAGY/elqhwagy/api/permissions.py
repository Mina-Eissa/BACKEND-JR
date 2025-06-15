from rest_framework.permissions import BasePermission,SAFE_METHODS
from .models import User
from .model.Choices import Roles

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        UserId = request.user.id
        Userins = User.objects.filter(id=UserId).first()
        return (Userins is not None and Userins.is_superuser) or request.method in SAFE_METHODS
    


