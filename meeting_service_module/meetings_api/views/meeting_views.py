import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings import Meeting
from ..serializers.meeting_serializers import MeetingSerializer

logger = logging.getLogger(__name__)

class MeetingListView(APIView):

    def get(self, request):
        try:
            company = request.user.company
            if not company:
                logger.warning(f"User {request.user.email} attempted to list meetings without a company association.")
                return Response(
                    {"error": "Your account is not associated with any company. Please contact support."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            meetings = Meeting.objects.filter(company=company)
            serializer = MeetingSerializer(meetings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing meetings for company {company if 'company' in locals() else 'None'}: {str(e)}")
            return Response({"error": "An unexpected error occurred while fetching meetings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        serializer = MeetingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.save()
            logger.info(f"New meeting '{meeting.title}' created by user {request.user.email} for company {request.user.company.company_name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingDetailsView(APIView):

    def get_object(self, id, company):
        return get_object_or_404(Meeting, id=id, company=company)

    def get(self, request, id):
        meeting = self.get_object(id, request.user.company)
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        meeting = self.get_object(id, request.user.company)
        serializer = MeetingSerializer(meeting, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Meeting ID {id} fully updated by {request.user.email}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        meeting = self.get_object(id, request.user.company)
        serializer = MeetingSerializer(meeting, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Meeting ID {id} partially updated by {request.user.email}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        meeting = self.get_object(id, request.user.company)
        meeting_title = meeting.title
        meeting.delete()
        logger.info(f"Meeting '{meeting_title}' (ID: {id}) deleted by {request.user.email}")
        return Response({"message": f"Meeting '{meeting_title}' has been successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
