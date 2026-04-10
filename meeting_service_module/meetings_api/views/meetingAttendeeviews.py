from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_attendee import MeetingAttendee
from shared.models import UserActivityLog
from ..serializers import MeetingAttendeeSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class MeetingAttendeeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_meeting_attendee'])
            instance = get_object_or_404(MeetingAttendee.active_objects, id=id, meeting__company=request.user.company)
            serializer = MeetingAttendeeSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_meeting_attendee'])
        paginate = request.query_params.get("paginate", "true")
        data = MeetingAttendee.active_objects.filter(meeting__company=request.user.company).order_by('id')
        
        params = ['meeting', 'employee', 'attendance_type', 'rsvp_status']
        for param in params:
            if param in request.query_params:
                value = request.query_params.get(param)
                data = data.filter(**{f"{param}__iexact": value})
            
        if paginate == "false":
            serializer = MeetingAttendeeSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, MeetingAttendeeSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Meeting Attendee')
    def post(self, request):
        check_permissions(request, ['add_meeting_attendee'])
        serializer = MeetingAttendeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.validated_data.get('meeting')
            if meeting and meeting.company != request.user.company:
                 return ResponseHandler.forbidden(message="Unauthorized: Meeting does not belong to your company.")
            
            serializer.save()
            return ResponseHandler.create_success('Meeting Attendee', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Meeting Attendee')
    def put(self, request, id=None):
        check_permissions(request, ['change_meeting_attendee'])
        instance = get_object_or_404(MeetingAttendee.active_objects, id=id, meeting__company=request.user.company)
        serializer = MeetingAttendeeSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Meeting Attendee', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Meeting Attendee')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_meeting_attendee'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = MeetingAttendee.active_objects.filter(id__in=ids, meeting__company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(MeetingAttendee, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Meeting Attendee"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Meeting Attendee")
