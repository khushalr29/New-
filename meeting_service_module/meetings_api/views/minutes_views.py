import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from shared.models.meetings.meeting_minutes import MeetingMinutes
from ..serializers.meeting_serializers import MeetingMinutesSerializer

logger = logging.getLogger(__name__)

class MinutesListView(APIView):
    """
    Handles retrieval and recording of meeting minutes.
    Data is isolated by the user's company affiliation.
    """

    def get(self, request):
        try:
            company = request.user.company
            if not company:
                return Response({"error": "Unauthorized: No company affiliation found."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve all minutes across all meetings for this company
            minutes = MeetingMinutes.objects.filter(company=company)
            serializer = MeetingMinutesSerializer(minutes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Failed to fetch meeting minutes.")
            return Response({"error": "Failure to load minutes from records."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        serializer = MeetingMinutesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Validate meeting-to-company mapping for security
            meeting = serializer.validated_data.get('meeting')
            if meeting and meeting.company != request.user.company:
                 logger.warning(f"Security Alert: User {request.user.email} attempted to post minutes for an unauthorized Meeting ID {meeting.id}")
                 return Response({"error": "Permission Denied: Meeting not found or unauthorized."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer.save(company=request.user.company)
            logger.info(f"Minutes recorded for meeting {meeting.id if meeting else 'Unknown'} by {request.user.email}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MinutesDetailsView(APIView):
    """
    Provides individual management of meeting minute entries.
    """

    def delete(self, request, id):
        minutes = get_object_or_404(MeetingMinutes, id=id, company=request.user.company)
        minutes.delete()
        logger.info(f"Meeting minute ID {id} deleted.")
        return Response({"message": "Meeting record successfully purged."}, status=status.HTTP_204_NO_CONTENT)
