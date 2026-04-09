from rest_framework.views import APIView
from shared.models import HRDocument, UserActivityLog
from ..serializers.hrDocumentSerializer import HRDocumentSerializer, HRDocumentListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class HRDocumentView(APIView):
    def get(self, request, pk=None):
        if pk:
            check_permissions(request, ['view_hr_document'])
            instance = get_object_or_404(HRDocument, id=pk, company=request.user.company)
            serializer = HRDocumentListSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_hr_document'])
        paginate = request.query_params.get("paginate", "true")
        data = HRDocument.objects.filter(company=request.user.company).order_by("-id")
        
        search = request.query_params.get("search")
        if search:
            data = data.filter(document_title__icontains=search)
        
        if paginate == "false":
            serializer = HRDocumentListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, HRDocumentListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'HR Document')
    def post(self, request):
        check_permissions(request, ['add_hr_document'])
        serializer = HRDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('HR Document')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'HR Document')
    def put(self, request, pk=None):
        check_permissions(request, ['change_hr_document'])
        instance = get_object_or_404(HRDocument, id=pk, company=request.user.company)
        serializer = HRDocumentSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('HR Document')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'HR Document')
    def delete(self, request):
        check_permissions(request, ['delete_hr_document'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = HRDocument.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(HRDocument, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("HR Document"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("HR Document")
