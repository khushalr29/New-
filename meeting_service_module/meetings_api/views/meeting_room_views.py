from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from shared.models.meetings.meeting_room import MeetingRoom
from ..serializers.meeting_serializers import MeetingRoomSerializer

class MeetingRoomListView(APIView):

    def get(self, request):
        user = self.request.user
        if not user.company:
             return Response({"error": "No company associated with user"}, status=status.HTTP_400_BAD_REQUEST)
        rooms = MeetingRoom.objects.filter(company=user.company)
        serializer = MeetingRoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MeetingRoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingRoomDetailsView(APIView):

    def get(self, request, id):
        room = get_object_or_404(MeetingRoom, id=id, company=request.user.company)
        serializer = MeetingRoomSerializer(room)
        return Response(serializer.data)
    
    def put(self, request, id):
        room = get_object_or_404(MeetingRoom, id=id, company=request.user.company)
        serializer = MeetingRoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        room = get_object_or_404(MeetingRoom, id=id, company=request.user.company)
        room.delete()
        return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
