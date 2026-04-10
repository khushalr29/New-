from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.leave_management.leave_application import LeaveApplication
from shared.models import UserActivityLog
from ..serializers.leaveApplicationSerializer import LeaveApplicationSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class LeaveApplicationView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_leave_application'])
            instance = get_object_or_404(LeaveApplication.active_objects, id=id, company=request.user.company)
            serializer = LeaveApplicationSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_leave_application'])
        paginate = request.query_params.get("paginate", "true")
        data = LeaveApplication.active_objects.filter(company=request.user.company).order_by('-created_at')
        
        params = ['leave_type', 'start_date', 'end_date', 'status']
        for param in params:
            if param in request.query_params:
                value = request.query_params.get(param)
                if param == 'status':
                    data = data.filter(status__iexact=value)
                else:
                    data = data.filter(**{param: value})
            
        if paginate == "false":
            serializer = LeaveApplicationSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, LeaveApplicationSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Leave Application')
    def post(self, request):
        check_permissions(request, ['add_leave_application'])
        serializer = LeaveApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company, employee=request.user.employee_profile)
            return ResponseHandler.create_success('Leave Application', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Leave Application')
    def put(self, request, id=None):
        check_permissions(request, ['change_leave_application'])
        instance = get_object_or_404(LeaveApplication.active_objects, id=id, company=request.user.company)
        serializer = LeaveApplicationSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Leave Application', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Leave Application')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_leave_application'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = LeaveApplication.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(LeaveApplication, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Leave Application"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Leave Application")