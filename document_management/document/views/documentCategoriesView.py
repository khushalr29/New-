from rest_framework.views import APIView
from shared.models import DocumentCategories, UserActivityLog
from ..serializers.documentCategoriesSerializer import DocumentCategoriesSerializer, DocumentCategoriesListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class DocumentCategoriesView(APIView):
    def get(self, request, pk=None):
        if pk:
            check_permissions(request, ['view_document_categories'])
            instance = get_object_or_404(DocumentCategories, id=pk, company=request.user.company)
            serializer = DocumentCategoriesListSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_document_categories'])
        paginate = request.query_params.get("paginate", "true")
        data = DocumentCategories.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(category_name__icontains=search)
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
    
        if paginate == "false":
            serializer = DocumentCategoriesListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, DocumentCategoriesListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Document Category')
    def post(self, request):
        check_permissions(request, ['add_document_categories'])
        serializer = DocumentCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Document Category')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Document Category')
    def put(self, request, pk=None):
        check_permissions(request, ['change_document_categories'])
        instance = get_object_or_404(DocumentCategories, id=pk, company=request.user.company)
        serializer = DocumentCategoriesSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Document Category')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Document Category')
    def delete(self, request):
        check_permissions(request, ['delete_document_categories'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = DocumentCategories.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(DocumentCategories, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Document Category"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Document Category")
