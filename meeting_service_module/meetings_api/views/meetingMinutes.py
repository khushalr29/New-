import logging
from rest_framework.views import APIView
from shared.models.meetings.meeting_minutes import MeetingMinutes
from ..serializers import MeetingMinutesSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

logger = logging.getLogger(__name__)

class MinutesListView(APIView):

    def get(self, request):
        try:
            # Base Queryset
            minutes = MeetingMinutes.active_objects.filter(company=request.user.company).order_by('-created_at')
            
            # Manual Searching
            search_query = request.query_params.get('search')
            if search_query:
                minutes = minutes.filter(
                    Q(topic__icontains=search_query) | 
                    Q(content__icontains=search_query) |
                    Q(key_decisions__icontains=search_query)
                )
            
            # Manual Filtering
            meeting = request.query_params.get('meeting')
            if meeting:
                minutes = minutes.filter(meeting_id=meeting)
                
            minutes_type = request.query_params.get('type')
            if minutes_type:
                minutes = minutes.filter(minutes_type=minutes_type)

            return paginate_queryset(minutes, request, MeetingMinutesSerializer)
        except Exception as e:
            return ResponseHandler.server_error(message="Failure to load minutes from records.", err=e)
    
    def post(self, request):
        serializer = MeetingMinutesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.validated_data.get('meeting')
            if meeting and meeting.company != request.user.company:
                 logger.warning(
                     f"Security Alert: User {request.user.email} attempted to post minutes "
                     f"for an unauthorized Meeting ID {meeting.id}"
                 )
                 return ResponseHandler.forbidden(message="Permission Denied: Meeting not found or unauthorized.")
            
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Meeting minutes", serializer.data)
        
        return ResponseHandler.create_failed(serializer.errors)

class MinutesDetailsView(APIView):

    def delete(self, request, id):
        try:
            minutes = MeetingMinutes.active_objects.get(id=id, company=request.user.company)
            minutes.delete()
            return ResponseHandler.delete_success("Meeting minutes")
        except MeetingMinutes.DoesNotExist:
            return ResponseHandler.not_found_error()


