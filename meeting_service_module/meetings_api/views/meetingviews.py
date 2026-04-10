from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings import Meeting
from shared.models import UserActivityLog
from ..serializers import MeetingSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class MeetingView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_meeting'])
            instance = get_object_or_404(Meeting.active_objects, id=id, company=request.user.company)
            serializer = MeetingSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_meeting'])
        paginate = request.query_params.get("paginate", "true")
        data = Meeting.active_objects.filter(company=request.user.company).order_by('-created_at')
        
        search_query = request.query_params.get('search')
        if search_query:
            data = data.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()
            
        params = ['meeting_type', 'meeting_room', 'meeting_date']
        for param in params:
            if param in request.query_params:
                value = request.query_params.get(param)
                data = data.filter(**{f"{param}__iexact": value})
        
        if paginate == "false":
            serializer = MeetingSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, MeetingSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Meeting')
    def post(self, request):
        check_permissions(request, ['add_meeting'])
        serializer = MeetingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Meeting', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Meeting')
    def put(self, request, id=None):
        check_permissions(request, ['change_meeting'])
        instance = get_object_or_404(Meeting.active_objects, id=id, company=request.user.company)
        serializer = MeetingSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Meeting', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Meeting')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_meeting'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = Meeting.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Meeting, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Meeting"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Meeting")
