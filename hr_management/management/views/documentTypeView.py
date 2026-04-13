from shared.models.hr_management.hr_masters import DocumentType
from shared.models.core.useractivity import UserActivityLog
from ..serializers.documentTypeSerializer import DocumentTypeSerializer, DocumentTypeListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class DocumentTypeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_document_type'])
            instance = get_object_or_404(DocumentType, id=id, company=request.user.company)
            serializer = DocumentTypeListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_document_type'])
        paginate = request.query_params.get("paginate", "true")
        data = DocumentType.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(document_type__icontains=search)
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)

        if paginate == "false":
            serializer = DocumentTypeListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, DocumentTypeListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_document_type'])
        serializer = DocumentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('document_type')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_document_type'])
        instance = get_object_or_404(DocumentType, id=id, company=request.user.company)
        serializer = DocumentTypeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('document_type')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_document_type'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = DocumentType.objects.filter(id__in=ids, company=request.user.company)
        deletable_ids = check_references_and_get_deletable_instances(queryset, 'document_type')
        if deletable_ids:
            queryset.filter(id__in=deletable_ids).update(deleted_at=timezone.now())
            return ResponseHandler.delete_success("document_type")
        return ResponseHandler.delete_failed(ResponseMessages.PROTECTED_RECORD)