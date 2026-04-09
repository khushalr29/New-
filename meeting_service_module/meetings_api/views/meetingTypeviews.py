from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_type import MeetingType
from ..serializers import MeetingTypeSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class MeetingTypeListView(APIView):

    def get(self, request):
     
        types = MeetingType.active_objects.filter(company=request.user.company).order_by('name')

        search_query = request.query_params.get('search')
        if search_query:
            types = types.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        return paginate_queryset(types, request, MeetingTypeSerializer)
    
    def post(self, request):
        serializer = MeetingTypeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Meeting type", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

class MeetingTypeDetailsView(APIView):
    def get(self, request, id):
        mtype = get_object_or_404(MeetingType.active_objects, id=id, company=request.user.company)
        serializer = MeetingTypeSerializer(mtype, context={'request': request})
        return ResponseHandler.success(serializer.data)
    
    def delete(self, request, id):
        mtype = get_object_or_404(MeetingType.active_objects, id=id, company=request.user.company)
        mtype.delete()
        return ResponseHandler.delete_success("Meeting type")


