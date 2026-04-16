from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management.hr_masters import Branch
from shared.models.core.useractivity import UserActivityLog
from ..serializers.branchSerializer import BranchSerializer, BranchListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class BranchView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_branch'])
            instance = get_object_or_404(Branch, id=id, company=request.user.company)
            serializer = BranchListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_branch'])
        paginate = request.query_params.get("paginate", "true")
        data = Branch.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(Q(branch_name__icontains=search)|
                               Q(branch_code__icontains=search)|
                               Q(address__icontains=search)|
                               Q(phone_number__icontains=search)|
                               Q(email__icontains=search))
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)

        if paginate == "false":
            serializer = BranchListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, BranchListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_branch'])
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('branch')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_branch'])
        instance = get_object_or_404(Branch, id=id, company=request.user.company)
        serializer = BranchSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('branch')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_branch'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Branch.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Branch, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("branch"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("branch")

class BranchStatusToggleView(APIView):
    def patch(self, request, id=None):
        check_permissions(request, ['change_branch'])
        instance = get_object_or_404(Branch, id=id, company=request.user.company)
        instance.status = "inactive" if instance.status == "active" else "active"
        instance.save()
        return ResponseHandler.success({"status": instance.status}, message="Status updated successfully")

class ActiveBranchView(APIView):
    def get(self, request):
        check_permissions(request, ['list_branch'])
        data = Branch.objects.filter(
            company=request.user.company, 
            status__iexact="active",
            deleted_at__isnull=True
        ).order_by("-id")
        serializer = BranchListSerializer(data, many=True)
        return ResponseHandler.list_success(serializer.data)