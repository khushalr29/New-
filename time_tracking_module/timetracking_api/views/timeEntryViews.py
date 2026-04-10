from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.models.time_tracking.time_entries import TimeEntries
from shared.models import UserActivityLog
from ..serializers.timeEntrySerializer import TimeEntriesSerializer
from django.db.models import Q
from shared.utils.common.pagination import paginate_queryset
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from django.utils import timezone

class TimeEntryView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_time_entry'])
            instance = get_object_or_404(TimeEntries.active_objects, id=id, company=request.user.company)
            serializer = TimeEntriesSerializer(instance, context={'request': request})
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_time_entry'])
        data = TimeEntries.active_objects.filter(company=request.user.company).order_by('-date')
        
        search = request.query_params.get('search')
        if search:
            data = data.filter(
                Q(date__icontains=search) | Q(project__icontains=search) | Q(description__icontains=search)
            ).distinct()
            
        params = ['date', 'project']
        for param in params:
            if param in request.query_params:
                data = data.filter(**{param: request.query_params.get(param)})
                
        return paginate_queryset(data, request, TimeEntriesSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Time Entry')
    def post(self, request):
        check_permissions(request, ['add_time_entry'])
        serializer = TimeEntriesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success("Time Entry", serializer.data)
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Time Entry')
    def put(self, request, id=None):
        check_permissions(request, ['change_time_entry'])
        instance = get_object_or_404(TimeEntries.active_objects, id=id, company=request.user.company)
        serializer = TimeEntriesSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success("Time Entry", serializer.data)
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Time Entry')
    def delete(self, request, id=None):
        check_permissions(request, ['delete_time_entry'])
        ids = request.data.get("ids", [])
        if id:
            ids.append(id)
            
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = TimeEntries.active_objects.filter(id__in=ids, company=request.user.company)
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Time Entry")

            