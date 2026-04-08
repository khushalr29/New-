from rest_framework.views import APIView
from shared.models import Shift, UserActivityLog
from ..serializers.shiftSerializer import ShiftSerializer, ShiftListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

class ShiftView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_shift'])
            instance = get_object_or_404(Shift, id=id, company=request.user.company)
            serializer = ShiftListSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_shift'])
        paginate = request.query_params.get("paginate", "true")
        data = Shift.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(shift_name__icontains=search)
        
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            try:
                start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                data = data.filter(created_at__date__gte=start, created_at__date__lte=end)
            except ValueError:
                pass

        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)

        shift_type = request.query_params.get("shift_type")
        if shift_type == "night":
            data = data.filter(is_night_shift=True)        
        elif shift_type == "day":
            data = data.filter(is_night_shift=False)
            
        if paginate == "false":
            serializer = ShiftListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, ShiftListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Shift')
    def post(self, request):
        check_permissions(request, ['add_shift'])
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_at=timezone.now(), company=request.user.company)
            return ResponseHandler.create_success('Shift')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Shift')
    def put(self, request, id=None):
        check_permissions(request, ['change_shift'])
        instance = get_object_or_404(Shift, id=id, company=request.user.company)
        serializer = ShiftSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Shift')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Shift')
    def delete(self, request):
        check_permissions(request, ['delete_shift'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        # Soft delete logic based on user's diff
        queryset = Shift.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Shift, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Shift"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Shift")
