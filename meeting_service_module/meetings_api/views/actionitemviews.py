from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.action_items import ActionItem
from shared.models import UserActivityLog
from ..serializers import ActionItemSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class ActionItemView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_action_item'])
            instance = get_object_or_404(ActionItem.active_objects, id=id, meeting__company=request.user.company)
            serializer = ActionItemSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_action_item'])
        paginate = request.query_params.get("paginate", "true")
        data = ActionItem.active_objects.filter(meeting__company=request.user.company).order_by('-due_date')
        
        search_query = request.query_params.get('search')
        if search_query:
            data = data.filter(
                Q(action_item_title__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()
            
        params = ['meeting', 'priority', 'assigned_to']
        for param in params:
            if param in request.query_params:
                value = request.query_params.get(param)
                if param == 'assigned_to':
                    data = data.filter(assigned_to_id=value)
                else:
                    data = data.filter(**{param: value})
        
        if paginate == "false":
            serializer = ActionItemSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, ActionItemSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Action Item')
    def post(self, request):
        check_permissions(request, ['add_action_item'])
        serializer = ActionItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.validated_data.get('meeting')
            if meeting and meeting.company != request.user.company:
                 return ResponseHandler.forbidden(message="Unauthorized: Meeting does not belong to your company.")
            
            serializer.save()
            return ResponseHandler.create_success('Action Item', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Action Item')
    def put(self, request, id=None):
        check_permissions(request, ['change_action_item'])
        instance = get_object_or_404(ActionItem.active_objects, id=id, meeting__company=request.user.company)
        serializer = ActionItemSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Action Item', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Action Item')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_action_item'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = ActionItem.active_objects.filter(id__in=ids, meeting__company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(ActionItem, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Action Item"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Action Item")
