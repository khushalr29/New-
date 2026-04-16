from rest_framework.views import APIView
from shared.models.hr_management.hr_masters import Designation
from shared.models.core.useractivity import UserActivityLog
from ..serializers.designationsSerializer import DesignationSerializer, DesignationListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class DesignationView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_designation'])
            instance = get_object_or_404(Designation, id=id, company=request.user.company)
            serializer = DesignationListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_designation'])
        paginate = request.query_params.get("paginate", "true")
        data = Designation.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(designation__icontains=search)
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)

        if paginate == "false":
            serializer = DesignationListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, DesignationListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_designation'])
        serializer = DesignationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('designation')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_designation'])
        instance = get_object_or_404(Designation, id=id, company=request.user.company)
        serializer = DesignationSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('designation')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_designation'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Designation.objects.filter(id__in=ids, company=request.user.company)
        deletable_ids = check_references_and_get_deletable_instances(queryset, 'designation')
        if deletable_ids:
            queryset.filter(id__in=deletable_ids).update(deleted_at=timezone.now())
            return ResponseHandler.delete_success("designation")
        return ResponseHandler.delete_failed(ResponseMessages.PROTECTED_RECORD)

class DesignationStatusToggleView(APIView):
    def patch(self, request, id=None):
        check_permissions(request, ['change_designation'])
        instance = get_object_or_404(Designation, id=id, company=request.user.company)
        instance.status = "inactive" if instance.status == "active" else "active"
        instance.save()
        return ResponseHandler.success({"status": instance.status}, message="Status updated successfully")

class ActiveDesignationView(APIView):
    def get(self, request):
        check_permissions(request, ['list_designation'])
        data = Designation.objects.filter(company=request.user.company, status="active").order_by("designation")
        serializer = DesignationListSerializer(data, many=True)
        return ResponseHandler.list_success(serializer.data)