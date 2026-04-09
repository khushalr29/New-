from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meeting_room import MeetingRoom
from ..serializers import MeetingRoomSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class MeetingRoomListView(APIView):

    def get(self, request):
        # Base Queryset
        rooms = MeetingRoom.active_objects.filter(company=request.user.company).order_by('name')
        
        # Manual Searching
        search_query = request.query_params.get('search')
        if search_query:
            rooms = rooms.filter(
                Q(name__icontains=search_query) | 
                Q(location__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Manual Filtering
        room_type = request.query_params.get('type')
        if room_type:
            rooms = rooms.filter(type=room_type)
            
        capacity = request.query_params.get('capacity')
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)

        return paginate_queryset(rooms, request, MeetingRoomSerializer)
    
    def post(self, request):
        serializer = MeetingRoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Meeting room", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

class MeetingRoomDetailsView(APIView):

    def get_object(self, id, company):
        try:
            return MeetingRoom.active_objects.get(id=id, company=company)
        except MeetingRoom.DoesNotExist:
            return None

    def get(self, request, id):
        room = self.get_object(id, request.user.company)
        if not room:
            return ResponseHandler.not_found_error()
        serializer = MeetingRoomSerializer(room, context={'request': request})
        return ResponseHandler.success(serializer.data)
    
    def put(self, request, id):
        room = self.get_object(id, request.user.company)
        if not room:
            return ResponseHandler.not_found_error()
        serializer = MeetingRoomSerializer(room, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Meeting room", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def delete(self, request, id):
        room = self.get_object(id, request.user.company)
        if not room:
            return ResponseHandler.not_found_error()
        room.delete()
        return ResponseHandler.delete_success("Meeting room")


