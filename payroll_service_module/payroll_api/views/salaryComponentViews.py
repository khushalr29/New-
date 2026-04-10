from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.payroll_management.salaryComponents import SalaryComponent
from shared.models import UserActivityLog
from ..serializers.salaryComponentSerializer import SalaryComponentSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class SalaryComponentView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_salary_component'])
            instance = get_object_or_404(SalaryComponent.active_objects, id=id, company=request.user.company)
            serializer = SalaryComponentSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_salary_component'])
        paginate = request.query_params.get("paginate", "true")
        data = SalaryComponent.active_objects.filter(company=request.user.company).order_by('name')
        
        search = request.query_params.get('search')
        if search:
            data = data.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            ).distinct()
            
        params = ['component_type', 'calculation_type', 'status']
        for param in params:
            if param in request.query_params:
                data = data.filter(**{param: request.query_params.get(param)})
        
        if paginate == "false":
            serializer = SalaryComponentSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, SalaryComponentSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Salary Component')
    def post(self, request):
        check_permissions(request, ['add_salary_component'])
        serializer = SalaryComponentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Salary Component', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Salary Component')
    def put(self, request, id=None):
        check_permissions(request, ['change_salary_component'])
        instance = get_object_or_404(SalaryComponent.active_objects, id=id, company=request.user.company)
        serializer = SalaryComponentSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Salary Component', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Salary Component')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_salary_component'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = SalaryComponent.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(SalaryComponent, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Salary Component"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Salary Component")