from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shared.models.meetings.meeting_room import MeetingRoom
from ..serializers import MeetingRoomSerializer

class MeetingRoomListView(APIView):

    def get(self, request):
       
        rooms = MeetingRoom.active_objects.filter(company=request.user.company)
        serializer = MeetingRoomSerializer(rooms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = MeetingRoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingRoomDetailsView(APIView):

    def get_object(self, id, company):
        return get_object_or_404(MeetingRoom.active_objects, id=id, company=company)

    def get(self, request, id):
        room = self.get_object(id, request.user.company)
        serializer = MeetingRoomSerializer(room, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        room = self.get_object(id, request.user.company)
        serializer = MeetingRoomSerializer(room, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        room = self.get_object(id, request.user.company)
        room.delete()
        return Response(
            {"message": "Room deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )

