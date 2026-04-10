from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.leave_management.leave_policies import LeavePolicy
from shared.models import UserActivityLog
from ..serializers.leavePolicySerializer import LeavePolicySerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class LeavePolicyView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_leave_policy'])
            instance = get_object_or_404(LeavePolicy.active_objects, id=id, company=request.user.company)
            serializer = LeavePolicySerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_leave_policy'])
        paginate = request.query_params.get("paginate", "true")
        data = LeavePolicy.active_objects.filter(company=request.user.company).order_by('-created_at')
        
        search = request.query_params.get('search')
        if search:
            data = data.filter(
                Q(policy_name__icontains=search)|
                Q(description__icontains=search)
            ).distinct()
            
        if paginate == "false":
            serializer = LeavePolicySerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, LeavePolicySerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Leave Policy')
    def post(self, request):
        check_permissions(request, ['add_leave_policy'])
        serializer = LeavePolicySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Leave Policy', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Leave Policy')
    def put(self, request, id=None):
        check_permissions(request, ['change_leave_policy'])
        instance = get_object_or_404(LeavePolicy.active_objects, id=id, company=request.user.company)
        serializer = LeavePolicySerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Leave Policy', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Leave Policy')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_leave_policy'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = LeavePolicy.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(LeavePolicy, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Leave Policy"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Leave Policy")