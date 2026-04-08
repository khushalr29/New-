from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_attendee import MeetingAttendee
from ..serializers.meeting_serializers import MeetingAttendeeSerializer

class AttendeeListView(APIView):

    def get(self, request):
        attendees = MeetingAttendee.objects.filter(meeting__company=request.user.company)
        serializer = MeetingAttendeeSerializer(attendees, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MeetingAttendeeSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['meeting'].company != request.user.company:
                 return Response({"error": "Unauthorized meeting"}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendeeDetailsView(APIView):

    def delete(self, request, id):
        attendee = get_object_or_404(MeetingAttendee, id=id, meeting__company=request.user.company)
        attendee.delete()
        return Response({"message": "Attendee removed successfully"}, status=status.HTTP_204_NO_CONTENT)
