from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meeting_minutes import MeetingMinutes
from shared.models import UserActivityLog
from ..serializers import MeetingMinutesSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class MeetingMinutesView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_meeting_minutes'])
            instance = get_object_or_404(MeetingMinutes.active_objects, id=id, company=request.user.company)
            serializer = MeetingMinutesSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_meeting_minutes'])
        paginate = request.query_params.get("paginate", "true")
        data = MeetingMinutes.active_objects.filter(company=request.user.company).order_by('-created_at')
        
        search_query = request.query_params.get('search')
        if search_query:
            data = data.filter(
                Q(topic__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(key_decisions__icontains=search_query)
            ).distinct()
            
        meeting = request.query_params.get('meeting')
        if meeting:
            data = data.filter(meeting_id=meeting)
            
        minutes_type = request.query_params.get('type')
        if minutes_type:
            data = data.filter(minutes_type=minutes_type)
        
        if paginate == "false":
            serializer = MeetingMinutesSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, MeetingMinutesSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Meeting Minutes')
    def post(self, request):
        check_permissions(request, ['add_meeting_minutes'])
        serializer = MeetingMinutesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.validated_data.get('meeting')
            if meeting and meeting.company != request.user.company:
                 return ResponseHandler.forbidden(message="Permission Denied: Meeting not found or unauthorized.")
            
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Meeting Minutes', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Meeting Minutes')
    def put(self, request, id=None):
        check_permissions(request, ['change_meeting_minutes'])
        instance = get_object_or_404(MeetingMinutes.active_objects, id=id, company=request.user.company)
        serializer = MeetingMinutesSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Meeting Minutes', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Meeting Minutes')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_meeting_minutes'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = MeetingMinutes.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(MeetingMinutes, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Meeting Minutes"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Meeting Minutes")
