from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_type import MeetingType
from ..serializers import MeetingTypeSerializer

class MeetingTypeListView(APIView):

    def get(self, request):
        
        types = MeetingType.active_objects.filter(company=request.user.company)
        serializer = MeetingTypeSerializer(types, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
      
        serializer = MeetingTypeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingTypeDetailsView(APIView):

    def get_object(self, id, company):
        return get_object_or_404(MeetingType.active_objects, id=id, company=company)

    def get(self, request, id):
        mtype = self.get_object(id, request.user.company)
        serializer = MeetingTypeSerializer(mtype, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        mtype = self.get_object(id, request.user.company)
        mtype.delete()
        return Response(
            {"message": "Meeting type deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )

