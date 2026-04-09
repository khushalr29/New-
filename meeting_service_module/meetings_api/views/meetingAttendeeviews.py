from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_attendee import MeetingAttendee
from ..serializers import MeetingAttendeeSerializer
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class AttendeeListView(APIView):

    def get(self, request):
        attendees = MeetingAttendee.active_objects.filter(meeting__company=request.user.company).order_by('id')
        params = ['meeting', 'employee', 'attendance_type', 'rsvp_status']
        for param in params:
            if param in request.query_params:
                value = request.query_params.get(param)
                filter_kwargs = {f"{param}__iexact": value}
                attendees = attendees.filter(**filter_kwargs)

        return paginate_queryset(attendees, request, MeetingAttendeeSerializer)
    
    def post(self, request):
        serializer = MeetingAttendeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.validated_data.get('meeting')
            if meeting.company != request.user.company:
                 return ResponseHandler.forbidden(message="Unauthorized: Meeting does not belong to your company.")
            
            serializer.save()
            return ResponseHandler.create_success("Attendee", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

class AttendeeDetailsView(APIView):

    def get(self, request, id):
        attendee = get_object_or_404(MeetingAttendee.active_objects, id=id, meeting__company=request.user.company)
        serializer = MeetingAttendeeSerializer(attendee, context={'request': request})
        return ResponseHandler.success(serializer.data)

    def put(self, request, id):
        attendee = get_object_or_404(MeetingAttendee.active_objects, id=id, meeting__company=request.user.company)
        serializer = MeetingAttendeeSerializer(attendee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Attendee", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def patch(self, request, id):
        attendee = get_object_or_404(MeetingAttendee.active_objects, id=id, meeting__company=request.user.company)
        serializer = MeetingAttendeeSerializer(attendee, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Attendee", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def delete(self, request, id):
        attendee = get_object_or_404(MeetingAttendee.active_objects, id=id, meeting__company=request.user.company)
        attendee.delete()
        return ResponseHandler.delete_success("Attendee")



