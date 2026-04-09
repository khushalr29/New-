from rest_framework.views import APIView
from shared.models.meetings.action_items import ActionItem
from ..serializers import ActionItemSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler

class ActionItemListView(APIView):

    def get(self, request):
        items = ActionItem.active_objects.filter(meeting__company=request.user.company).order_by('-due_date')
        
        search_query = request.query_params.get('search')
        if search_query:
            items = items.filter(
                Q(action_item_title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        meeting = request.query_params.get('meeting')
        if meeting:
            items = items.filter(meeting_id=meeting)
            
        priority = request.query_params.get('priority')
        if priority:
            items = items.filter(priority=priority)
            
        assigned_to = request.query_params.get('assigned_to')
        if assigned_to:
            items = items.filter(assigned_to_id=assigned_to)

        return paginate_queryset(items, request, ActionItemSerializer)
    
    def post(self, request):
        serializer = ActionItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.validated_data.get('meeting')
            if meeting.company != request.user.company:
                 return ResponseHandler.forbidden(message="Unauthorized: Meeting does not belong to your company.")
            
            serializer.save()
            return ResponseHandler.create_success("Action item", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

class ActionItemDetailsView(APIView):

    def get_object(self, id, company):
        try:
            return ActionItem.active_objects.get(id=id, meeting__company=company)
        except ActionItem.DoesNotExist:
            return None

    def get(self, request, id):
        item = self.get_object(id, request.user.company)
        if not item:
            return ResponseHandler.not_found_error()
        serializer = ActionItemSerializer(item, context={'request': request})
        return ResponseHandler.success(serializer.data)

    def put(self, request, id):
        item = self.get_object(id, request.user.company)
        if not item:
            return ResponseHandler.not_found_error()
        serializer = ActionItemSerializer(item, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Action item", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    def patch(self, request, id):
        item = self.get_object(id, request.user.company)
        if not item:
            return ResponseHandler.not_found_error()
        serializer = ActionItemSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success("Action item", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)
    
    def delete(self, request, id):
        item = self.get_object(id, request.user.company)
        if not item:
            return ResponseHandler.not_found_error()
        item.delete()
        return ResponseHandler.delete_success("Action item")


