from rest_framework.views import APIView
from shared.models import Employee, UserActivityLog
from ..serializers.employeeSerializer import EmployeeSerializer, EmployeeListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from django.shortcuts import get_object_or_404
from django.utils import timezone

class EmployeeView(APIView):
    def get(self, request, pk=None):
        if pk:
            check_permissions(request, ['view_employee'])
            instance = get_object_or_404(Employee, id=pk, company=request.user.company)
            serializer = EmployeeSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_employee'])
        paginate = request.query_params.get("paginate", "true")
        data = Employee.active_objects.filter(company=request.user.company).order_by("-id")
        
        search = request.query_params.get("search")
        if search:
            data = data.filter(full_name__icontains=search)
        
        if paginate == "false":
            serializer = EmployeeListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, EmployeeListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Employee')
    def post(self, request):
        check_permissions(request, ['add_employee'])
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Employee', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Employee')
    def put(self, request, pk=None):
        check_permissions(request, ['change_employee'])
        instance = get_object_or_404(Employee, id=pk, company=request.user.company)
        serializer = EmployeeSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Employee', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Employee')
    def delete(self, request):
        check_permissions(request, ['delete_employee'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = Employee.objects.filter(id__in=ids, company=request.user.company)
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Employee")

class EmployeeStatusToggleView(APIView):
    def patch(self, request, pk):
        check_permissions(request, ['change_employee'])
        instance = get_object_or_404(Employee, id=pk, company=request.user.company)
        instance.is_enabled = not instance.is_enabled
        instance.save()
        return ResponseHandler.success({"is_enabled": instance.is_enabled}, message="Status updated successfully")
