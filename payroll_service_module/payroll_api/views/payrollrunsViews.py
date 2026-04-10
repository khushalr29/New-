from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.payroll_management.payrollRuns import PayrollRun
from shared.models import UserActivityLog
from ..serializers.payrollRunSerializer import PayrollRunSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class PayrollRunView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_payroll_run'])
            instance = get_object_or_404(PayrollRun.active_objects, id=id, company=request.user.company)
            serializer = PayrollRunSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_payroll_run'])
        paginate = request.query_params.get("paginate", "true")
        data = PayrollRun.active_objects.filter(company=request.user.company).order_by('-pay_date')
        
        search = request.query_params.get('search')
        if search:
            data = data.filter(
                Q(title__icontains=search) | Q(notes__icontains=search)
            ).distinct()
            
        params = ['payroll_frequency']
        for param in params:
            if param in request.query_params:
                data = data.filter(**{param: request.query_params.get(param)})
        
        if paginate == "false":
            serializer = PayrollRunSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, PayrollRunSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Payroll Run')
    def post(self, request):
        check_permissions(request, ['add_payroll_run'])
        serializer = PayrollRunSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Payroll Run', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Payroll Run')
    def put(self, request, id=None):
        check_permissions(request, ['change_payroll_run'])
        instance = get_object_or_404(PayrollRun.active_objects, id=id, company=request.user.company)
        serializer = PayrollRunSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Payroll Run', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Payroll Run')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_payroll_run'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = PayrollRun.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(PayrollRun, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Payroll Run"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Payroll Run")