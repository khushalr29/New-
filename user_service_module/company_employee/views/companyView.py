from rest_framework.views import APIView
from shared.models import Company, UserActivityLog
from ..serializers.companySerializer import CompanySerializer, CompanyListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from django.shortcuts import get_object_or_404
from django.utils import timezone

class CompanyView(APIView):
    def get(self, request, pk=None):
        if pk:
            check_permissions(request, ['view_company'])
            instance = get_object_or_404(Company, id=pk)
            serializer = CompanySerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_company'])
        paginate = request.query_params.get("paginate", "true")
        data = Company.objects.all().order_by("-id")
        
        search = request.query_params.get("search")
        if search:
            data = data.filter(company_name__icontains=search)
        
        if paginate == "false":
            serializer = CompanyListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, CompanyListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'Company')
    def post(self, request):
        check_permissions(request, ['add_company'])
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.create_success('Company')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Company')
    def put(self, request, pk=None):
        check_permissions(request, ['change_company'])
        instance = get_object_or_404(Company, id=pk)
        serializer = CompanySerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Company')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Company')
    def delete(self, request):
        check_permissions(request, ['delete_company'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = Company.objects.filter(id__in=ids)
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Company")

class CompanyStatusToggleView(APIView):
    def patch(self, request, pk):
        check_permissions(request, ['change_company'])
        instance = get_object_or_404(Company, id=pk)
        instance.is_enabled = not instance.is_enabled
        instance.save()
        return ResponseHandler.success({"is_enabled": instance.is_enabled}, message="Status updated successfully")
