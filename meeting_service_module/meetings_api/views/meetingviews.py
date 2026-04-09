from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings import Meeting
from ..serializers import MeetingSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class MeetingListView(APIView):

    def get(self,request):
        meeting = Meeting.active_objects.filter(company=request.user.company).order_by('created_at')
        search_query = request.query_params.get('search')
        if search_query:
            meeting = meeting.filter(
                Q(meeting_title__icontains=search_query) |
                Q(meeting_id__icontains=search_query)|
                Q(decription__icontains=search_query)
        ).distinct()
        parms = ['meeting_type', 'meeting_room', 'meeting_date']
        for parm in parms:
            if parm in request.query_params:
                value = request.query_params.get(parm)
                filter_kwargs = {f"{parm}__iexact": value}
                meeting = meeting.filter(**filter_kwargs)
        return paginate_queryset(meeting, request, MeetingSerializer)
    def post(self, request):
        serializer = MeetingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Meeting", serializer.data)
        
        return ResponseHandler.create_failed(serializer.errors)

class MeetingDetailsView(APIView):

    def get(self, request, id):
        meeting = get_object_or_404(Meeting.active_objects, id=id, company=request.user.company)
        serializer = MeetingSerializer(meeting, context={'request': request})
        return ResponseHandler.success(serializer.data)
    
    def put(self, request, id):
        meeting = get_object_or_404(Meeting.active_objects, id=id, company=request.user.company)
        serializer = MeetingSerializer(meeting, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Meeting", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def patch(self, request, id):
        meeting = get_object_or_404(Meeting.active_objects, id=id, company=request.user.company)
        serializer = MeetingSerializer(meeting, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Meeting", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def delete(self, request, id):
        meeting = get_object_or_404(Meeting.active_objects, id=id, company=request.user.company)
        meeting.delete()
        return ResponseHandler.delete_success("Meeting")


