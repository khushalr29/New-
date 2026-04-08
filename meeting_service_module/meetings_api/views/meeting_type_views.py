from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_type import MeetingType
from ..serializers.meeting_serializers import MeetingTypeSerializer

class MeetingTypeListView(APIView):

    def get(self, request):
        user = self.request.user
        if not user.company:
             return Response({"error": "No company associated with user"}, status=status.HTTP_400_BAD_REQUEST)
        types = MeetingType.objects.filter(company=user.company)
        serializer = MeetingTypeSerializer(types, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MeetingTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingTypeDetailsView(APIView):

    def get(self, request, id):
        mtype = get_object_or_404(MeetingType, id=id, company=request.user.company)
        serializer = MeetingTypeSerializer(mtype)
        return Response(serializer.data)
    
    def delete(self, request, id):
        mtype = get_object_or_404(MeetingType, id=id, company=request.user.company)
        mtype.delete()
        return Response({"message": "Meeting type deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
