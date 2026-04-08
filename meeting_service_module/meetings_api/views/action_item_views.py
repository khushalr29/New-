from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from shared.models.meetings.action_items import ActionItem
from ..serializers.meeting_serializers import ActionItemSerializer

class ActionItemListView(APIView):

    def get(self, request):
        items = ActionItem.objects.filter(meeting__company=request.user.company)
        serializer = ActionItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ActionItemSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['meeting'].company != request.user.company:
                 return Response({"error": "Unauthorized meeting"}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActionItemDetailsView(APIView):

    def patch(self, request, id):
        item = get_object_or_404(ActionItem, id=id, meeting__company=request.user.company)
        serializer = ActionItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        item = get_object_or_404(ActionItem, id=id, meeting__company=request.user.company)
        item.delete()
        return Response({"message": "Action item removed successfully"}, status=status.HTTP_204_NO_CONTENT)
