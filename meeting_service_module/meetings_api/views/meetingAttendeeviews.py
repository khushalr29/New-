from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_attendee import MeetingAttendee
from ..serializers import MeetingAttendeeSerializer
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class AttendeeListView(APIView):

    def get(self, request):
        attendees = MeetingAttendee.active_objects.filter(meeting__company=request.user.company).order_by('id')
        parms = ['meeting', 'employee', 'attendance_type', 'rsvp_status']
        for parms in parms:
            if parms in parms in request.query_parms:
                value = request.query_farms.get(parms)
                filter_kwargs = {f"{parms}__iexact": value}
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
    def get_object(self, id, company):
        try:
            return MeetingAttendee.active_objects.get(id=id, meeting__company=company)
        except MeetingAttendee.DoesNotExist:
            return None

    def get(self, request, id):
        attendee = self.get_object(id, request.user.company)
        if not attendee:
            return ResponseHandler.not_found_error()
        serializer = MeetingAttendeeSerializer(attendee, context={'request': request})
        return ResponseHandler.success(serializer.data)

    def put(self, request, id):
        attendee = self.get_object(id, request.user.company)
        if not attendee:
            return ResponseHandler.not_found_error()
        serializer = MeetingAttendeeSerializer(attendee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Attendee", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def patch(self, request, id):
        attendee = self.get_object(id, request.user.company)
        if not attendee:
            return ResponseHandler.not_found_error()
        serializer = MeetingAttendeeSerializer(attendee, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Attendee", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def delete(self, request, id):
        attendee = self.get_object(id, request.user.company)
        if not attendee:
            return ResponseHandler.not_found_error()
        attendee.delete()
        return ResponseHandler.delete_success("Attendee")



