from shared.models import User
from ..renders import UserRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from shared.utils.common import check_permissions
from shared.utils.response import ResponseHandler,ResponseMessages
from ..serializers.permissionsSearializer import PermissionSerializer,UserPermissionsSerializer

class PermissionListView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request):
        required_permissions = ['list_permission']
        check_permissions(request, required_permissions)

        user = request.user
        user_company = getattr(user, 'company', None)

        if user_company:
            permissions = user.user_permissions.all()
        else:
            permissions = Permission.objects.all()

        permissions = permissions.order_by('name')
        serializer = PermissionSerializer(permissions, many=True)
        return ResponseHandler.list_success(serializer.data)

class PermissionDetailView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, id):
        required_permissions = ['view_permission']
        check_permissions(request, required_permissions)
        
        try:
            permission = Permission.objects.get(id=id)
            serializer = PermissionSerializer(permission)
            return Response(serializer.data)
        except Permission.DoesNotExist:
            return ResponseHandler.not_found_error()
        
class ManagePermissionsForUserView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, id):
        required_permissions = ['add_permission']
        check_permissions(request, required_permissions)

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return ResponseHandler.not_found(message=ResponseMessages.USER_NOT_FOUND)

        permission_ids_to_assign = request.data.get('assign_permissions', [])
        permission_ids_to_remove = request.data.get('remove_permissions', [])

        if not permission_ids_to_assign and not permission_ids_to_remove:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_PERMISSIONS_PROVIDED)

        messages = []

        for permission_id in permission_ids_to_assign:
            try:
                permission = Permission.objects.get(id=permission_id)
                user.user_permissions.add(permission)
                messages.append(f"Assigned permission ID {permission_id}")
            except Permission.DoesNotExist:
                return ResponseHandler.not_found(
                    message=ResponseMessages.PERMISSION_NOT_FOUND.format(id=permission_id)
                )

        for permission_id in permission_ids_to_remove:
            try:
                permission = Permission.objects.get(id=permission_id)
                user.user_permissions.remove(permission)
                messages.append(f"Removed permission ID {permission_id}")
            except Permission.DoesNotExist:
                return ResponseHandler.not_found(
                    message=ResponseMessages.PERMISSION_NOT_FOUND.format(id=permission_id)
                )

        user.save()
        return ResponseHandler.success(message=ResponseMessages.PERMISSION_ASSIGN_SUCCESS)

class UserPermissionsListView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id):
        required_permissions = ['view_user']
        check_permissions(request, required_permissions)

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return ResponseHandler.not_found(message=ResponseMessages.USER_NOT_FOUND)

        serializer = UserPermissionsSerializer(user)
        return ResponseHandler.list_success(data=serializer.data)   
    