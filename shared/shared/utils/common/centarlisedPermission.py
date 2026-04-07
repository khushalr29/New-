from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from ..response import ResponseHandler, ResponseMessages

def check_permissions(request, required_permissions):
    if not request.user.is_authenticated:
        raise NotAuthenticated(ResponseMessages.unauthorized)
    
    if not required_permissions:
        return
    
    if not any(
        request.user.has_permission(perm) or request.user.is_superuser for perm in required_permissions
    ):
        raise PermissionDenied(ResponseMessages.forbidden())

def base_permission_view(request):
    required_permissions = []
    check_permissions(request, required_permissions)
    return ResponseHandler.success(message=ResponseMessages.access_granted)
