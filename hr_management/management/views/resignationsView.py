from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Resignations
from shared.models.core.useractivity import UserActivityLog
from ..serializers.resignationsSerializer import ResignationsSerializer, ResignationsListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class ResignationView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_resignations'])
            instance = get_object_or_404(Resignations, id=id, company=request.user.company)
            serializer = ResignationsListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_resignations'])
        paginate = request.query_params.get("paginate", "true")
        data = Resignations.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(description__icontains=search)|
            Q(resignation_reason__icontains = search)|
            Q(employee__full_name__icontains = search)
        )

        if employee := request.query_params.get("employee"):
            data = data.filter(employee__full_name = employee)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if date_from := request.query_params.get("date_from"):
            data = data.filter(resignation_date__gte=date_from)

        if date_to := request.query_params.get("date_to"):
            data = data.filter(resignation_date__lte=date_to)

        if paginate == "false":
            serializer = ResignationsListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, ResignationsListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_resignations'])
        serializer = ResignationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('resignations')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_resignations'])
        instance = get_object_or_404(Resignations, id=id, company=request.user.company)
        serializer = ResignationsSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('resignations')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_resignations'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Resignations.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Resignations, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("resignations"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("resignations")