from rest_framework.views import APIView
from shared.models import AttendanceRegularization
from ..serializers.attendenceRegularizationSerializer import AttendanceRegularizationSerializer, AttendanceRegularizationListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

class AttendanceRegularizationView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_attendance_regularization'])
            instance = get_object_or_404(AttendanceRegularization, id=id, company=request.user.company)
            serializer = AttendanceRegularizationListSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_attendance_regularization'])
        paginate = request.query_params.get("paginate", "true")
        data = AttendanceRegularization.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(employee__full_name__icontains=search)
        
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        if date_from and date_to:
            try:
                start = datetime.datetime.strptime(date_from, '%H:%M:%S').time()
                end = datetime.datetime.strptime(date_to, '%H:%M:%S').time()
                data = data.filter(request_clock_in__gte=start, request_clock_out__lte=end)
            except ValueError:
                pass

        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
     
        if paginate == "false":
            serializer = AttendanceRegularizationListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AttendanceRegularizationListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'AttendanceRegularization')
    def post(self, request):
        check_permissions(request, ['add_attendance_regularization'])
        serializer = AttendanceRegularizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_at=timezone.now(), company=request.user.company)
            return ResponseHandler.create_success('AttendanceRegularization')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'AttendanceRegularization')
    def put(self, request, id=None):
        check_permissions(request, ['change_attendance_regularization'])
        instance = get_object_or_404(AttendanceRegularization, id=id, company=request.user.company)
        serializer = AttendanceRegularizationSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('AttendanceRegularization')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'AttendanceRegularization')
    def delete(self, request):
        check_permissions(request, ['delete_attendance_regularization'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = AttendanceRegularization.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(AttendanceRegularization, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("AttendanceRegularization"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("AttendanceRegularization")