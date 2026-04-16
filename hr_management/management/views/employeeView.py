from rest_framework.views import APIView
from shared.models import Employee
from shared.models.core.useractivity import UserActivityLog
from ..serializers.employeeSerializer import EmployeeSerializer, EmployeeListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class EmployeeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_employee'])
            instance = get_object_or_404(Employee, id=id, company=request.user.company)
            serializer = EmployeeListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_employee'])
        paginate = request.query_params.get("paginate", "true")
        data = Employee.objects.filter(company=request.user.company).order_by("-id")
        if search := request.query_params.get("search"):
            data = data.filter(full_name__icontains=search)
        if status := request.query_params.get("status"):
            data = data.filter(status=status)
        if gender := request.query_params.get("gender"):
            data = data.filter(gender=gender)
        if department_id := request.query_params.get("department_id"):
            data = data.filter(department_id=department_id)
        if designation_id := request.query_params.get("designation_id"):
            data = data.filter(designation_id=designation_id)
        if branch_id := request.query_params.get("branch_id"):
            data = data.filter(branch_id=branch_id)
        if employee_type_id := request.query_params.get("employee_type_id"):
            data = data.filter(employee_type_id=employee_type_id)
        if employee_status_id := request.query_params.get("employee_status_id"):
            data = data.filter(employee_status_id=employee_status_id)
        if paginate == "false":
            serializer = EmployeeListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, EmployeeListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_employee'])
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('employee')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_employee'])
        instance = get_object_or_404(Employee, id=id, company=request.user.company)
        serializer = EmployeeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('employee')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_employee'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Employee.objects.filter(id__in=ids, company=request.user.company)
        deletable_ids = check_references_and_get_deletable_instances(queryset, 'employee')
        if deletable_ids:
            queryset.filter(id__in=deletable_ids).update(deleted_at=timezone.now())
            return ResponseHandler.delete_success("employee")
        return ResponseHandler.delete_failed(ResponseMessages.PROTECTED_RECORD)

class ActiveEmployeeView(APIView):
    def get(self, request):
        check_permissions(request, ['list_employee'])
        data = Employee.objects.filter(company=request.user.company, status='active').order_by("-id")
        serializer = EmployeeListSerializer(data, many=True)
        return ResponseHandler.list_success(serializer.data)