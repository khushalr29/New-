from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.meetings.meetings_type import MeetingType
from shared.models import UserActivityLog
from ..serializers import MeetingTypeSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.utils import timezone

class MeetingTypeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_meeting_type'])
            instance = get_object_or_404(MeetingType.active_objects, id=id, company=request.user.company)
            serializer = MeetingTypeSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_meeting_type'])
        paginate = request.query_params.get("paginate", "true")
        data = MeetingType.active_objects.filter(company=request.user.company).order_by('name')
        
        search_query = request.query_params.get('search')
        if search_query:
            data = data.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()
            
        if paginate == "false":
            serializer = MeetingTypeSerializer(data, many=True, context={'request': request})
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, MeetingTypeSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Meeting Type')
    def post(self, request):
        check_permissions(request, ['add_meeting_type'])
        serializer = MeetingTypeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Meeting Type', serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Meeting Type')
    def put(self, request, id=None):
        check_permissions(request, ['change_meeting_type'])
        instance = get_object_or_404(MeetingType.active_objects, id=id, company=request.user.company)
        serializer = MeetingTypeSerializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Meeting Type', serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Meeting Type')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_meeting_type'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = MeetingType.active_objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(MeetingType, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Meeting Type"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Meeting Type")
