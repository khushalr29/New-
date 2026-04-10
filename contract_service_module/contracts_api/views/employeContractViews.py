from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.contract_management.employee_contract import EmployeeContract
from shared.models import UserActivityLog
from ..serializers.employeContractserializer import EmployeeContractSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class EmployeeContractView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_employee_contract'])
            instance = get_object_or_404(EmployeeContract.active_objects, id=id, company=request.user.company)
            serializer = EmployeeContractSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_employee_contract'])
        paginate = request.query_params.get("paginate", "true")
        data = EmployeeContract.active_objects.filter(company=request.user.company).order_by('-start_date')
        
        employee = request.query_params.get('employee')
        if employee:
            data = data.filter(employee_id=employee)
        
        contract_type = request.query_params.get('type')
        if contract_type:
            data = data.filter(contract_type_id=contract_type)
            
        if paginate == "false":
            serializer = EmployeeContractSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, EmployeeContractSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Employee Contract')
    def post(self, request):
        check_permissions(request, ['add_employee_contract'])
        serializer = EmployeeContractSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            if start_date and end_date and start_date >= end_date:
                return ResponseHandler.create_failed(message="End date must be after start date.")
                
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Employee Contract', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Employee Contract')
    def put(self, request, id=None):
        check_permissions(request, ['change_employee_contract'])
        instance = get_object_or_404(EmployeeContract.active_objects, id=id, company=request.user.company)
        serializer = EmployeeContractSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Employee Contract', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Employee Contract')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_employee_contract'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = EmployeeContract.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(EmployeeContract, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Employee Contract"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Employee Contract")