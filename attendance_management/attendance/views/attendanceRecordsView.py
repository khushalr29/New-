from rest_framework.views import APIView
from shared.models import Attendance, UserActivityLog
from ..serializers.attendanceRecordSerializer import AttendanceRecordSerializer, AttendanceRecordListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

class AttendanceRecordsView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_attendance'])
            instance = get_object_or_404(Attendance, id=id, company=request.user.company)
            serializer = AttendanceRecordListSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_attendance'])
        paginate = request.query_params.get("paginate", "true")
        data = Attendance.active_objects.filter(company=request.user.company).order_by("-id")
        
        search = request.query_params.get("search")
        if search:
            data = data.filter(employee__full_name__icontains=search)
        
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        if date_from and date_to:
            try:
                start = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
                end = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
                data = data.filter(date__range=[start, end])
            except ValueError:
                pass

        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
     
        if paginate == "false":
            serializer = AttendanceRecordListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AttendanceRecordListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Attendance Record')
    def post(self, request):
        check_permissions(request, ['add_attendance'])
        serializer = AttendanceRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Attendance Record', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Attendance Record')
    def put(self, request, id=None):
        check_permissions(request, ['change_attendance'])
        instance = get_object_or_404(Attendance, id=id, company=request.user.company)
        serializer = AttendanceRecordSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Attendance Record', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Attendance Record')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_attendance'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = Attendance.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Attendance, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Attendance Record"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Attendance Record")
