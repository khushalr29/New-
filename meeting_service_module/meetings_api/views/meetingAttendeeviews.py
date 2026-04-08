from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_attendee import MeetingAttendee
from ..serializers import MeetingAttendeeSerializer

class AttendeeListView(APIView):

    def get(self, request):
       
        attendees = MeetingAttendee.active_objects.filter(meeting__company=request.user.company)
        serializer = MeetingAttendeeSerializer(attendees, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
       
        serializer = MeetingAttendeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
           
            meeting = serializer.validated_data.get('meeting')
            if meeting.company != request.user.company:
                 return Response(
                     {"error": "Unauthorized: Meeting does not belong to your company."}, 
                     status=status.HTTP_403_FORBIDDEN
                 )
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendeeDetailsView(APIView):

    def delete(self, request, id):
       
        attendee = get_object_or_404(MeetingAttendee.active_objects, id=id, meeting__company=request.user.company)
        attendee.delete()
        return Response(
            {"message": "Attendee removed successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )

