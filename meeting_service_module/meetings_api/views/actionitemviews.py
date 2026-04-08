from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shared.models.meetings.action_items import ActionItem
from ..serializers import ActionItemSerializer

class ActionItemListView(APIView):

    def get(self, request):
       
        items = ActionItem.active_objects.filter(meeting__company=request.user.company)
        serializer = ActionItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
       
        serializer = ActionItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            
            meeting = serializer.validated_data.get('meeting')
            if meeting.company != request.user.company:
                 return Response(
                     {"error": "Unauthorized: Meeting does not belong to your company."}, 
                     status=status.HTTP_403_FORBIDDEN
                 )
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActionItemDetailsView(APIView):

    def get_object(self, id, company):
        return get_object_or_404(ActionItem.active_objects, id=id, meeting__company=company)

    def patch(self, request, id):
      
        item = self.get_object(id, request.user.company)
        serializer = ActionItemSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        
        item = self.get_object(id, request.user.company)
        item.delete()
        return Response(
            {"message": "Action item removed successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )

