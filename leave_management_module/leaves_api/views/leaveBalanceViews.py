from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.leave_management.leave_balances import LeaveBalance
from shared.models import UserActivityLog
from ..serializers.leaveBalanceSerializer import LeaveBalanceSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class LeaveBalanceView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_leave_balance'])
            instance = get_object_or_404(LeaveBalance.active_objects, id=id, company=request.user.company)
            serializer = LeaveBalanceSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_leave_balance'])
        paginate = request.query_params.get("paginate", "true")
        data = LeaveBalance.active_objects.filter(company=request.user.company).order_by('-created_at')
        
        search = request.query_params.get('search')
        if search:
            data = data.filter(
                Q(leave_type__name__icontains=search)|
                Q(employee__full_name__icontains=search)
            ).distinct()
            
        if paginate == "false":
            serializer = LeaveBalanceSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, LeaveBalanceSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Leave Balance')
    def post(self, request):
        check_permissions(request, ['add_leave_balance'])
        serializer = LeaveBalanceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Leave Balance', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Leave Balance')
    def put(self, request, id=None):
        check_permissions(request, ['change_leave_balance'])
        instance = get_object_or_404(LeaveBalance.active_objects, id=id, company=request.user.company)
        serializer = LeaveBalanceSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Leave Balance', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Leave Balance')
    def delete(self, request):
        check_permissions(request, ['delete_leave_balance'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = LeaveBalance.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(LeaveBalance, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Leave Balance"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Leave Balance")