from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings import Meeting
from ..serializers import MeetingSerializer

class MeetingListView(APIView):

    def get(self, request):
    
        meetings = Meeting.active_objects.filter(company=request.user.company)
        serializer = MeetingSerializer(meetings, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
       
        serializer = MeetingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingDetailsView(APIView):

    def get_object(self, id, company):
        return get_object_or_404(Meeting.active_objects, id=id, company=company)

    def get(self, request, id):
        meeting = self.get_object(id, request.user.company)
        serializer = MeetingSerializer(meeting, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        meeting = self.get_object(id, request.user.company)
        serializer = MeetingSerializer(meeting, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        meeting = self.get_object(id, request.user.company)
        serializer = MeetingSerializer(meeting, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        meeting = self.get_object(id, request.user.company)
        meeting_title = meeting.title
        meeting.delete()
        return Response(
            {"message": f"Meeting '{meeting_title}' has been successfully deleted."}, 
            status=status.HTTP_204_NO_CONTENT
        )

