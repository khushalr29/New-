from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Transfer
from shared.models.core.useractivity import UserActivityLog
from ..serializers.transferSerializer import TransferSerializer, TransferListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class TransferView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_transfer'])
            instance = get_object_or_404(Transfer, id=id, company=request.user.company)
            serializer = TransferListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_transfer'])
        paginate = request.query_params.get("paginate", "true")
        data = Transfer.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(employee__full_name__icontains=search)
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)

        if employee := request.query_params.get("employee"):
            data = data.filter(employee__full_name=employee)

        if branch := request.query_params.get("branch"):
            data = data.filter(new_branch__branch_name__icontains=branch)

        if department := request.query_params.get("department"):
            data = data.filter(new_department__department__icontains= department)
        
        if start_date := request.query_params.get("start_date"):
            data = data.filter(transfer_date__gte=start_date)
        
        if end_date := request.query_params.get("end_date"):
            data = data.filter(transfer_date__lte=end_date)

        if paginate == "false":
            serializer = TransferListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, TransferListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_transfer'])
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('transfer')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_transfer'])
        instance = get_object_or_404(Transfer, id=id, company=request.user.company)
        serializer = TransferSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('transfer')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_transfer'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Transfer.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Transfer, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("transfer"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("transfer")