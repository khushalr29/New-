from rest_framework.views import APIView
from shared.models import Role, UserActivityLog
from ..serializers.roleSerializer import RoleSerializer, RoleListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from django.shortcuts import get_object_or_404
from django.utils import timezone

class RoleView(APIView):
    def get(self, request, pk=None):
        if pk:
            check_permissions(request, ['view_role'])
            instance = get_object_or_404(Role, id=pk, company=request.user.company)
            serializer = RoleSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_role'])
        data = Role.objects.filter(company=request.user.company).order_by("-id")
        serializer = RoleListSerializer(data, many=True)
        return ResponseHandler.list_success(serializer.data)

    @log_activity(UserActivityLog.CREATE, 'Role')
    def post(self, request):
        check_permissions(request, ['add_role'])
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Role')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Role')
    def put(self, request, pk=None):
        check_permissions(request, ['change_role'])
        instance = get_object_or_404(Role, id=pk, company=request.user.company)
        serializer = RoleSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Role')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Role')
    def delete(self, request):
        check_permissions(request, ['delete_role'])
        ids = request.data.get("ids", [])
        if not ids:
            return ResponseHandler.bad_request()
        
        Role.objects.filter(id__in=ids, company=request.user.company).update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Role")
