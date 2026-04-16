from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Warning
from shared.models.core.useractivity import UserActivityLog
from ..serializers.warningSerializer import WarningSerializer, WarningListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class WarningView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_warning'])
            instance = get_object_or_404(Warning, id=id, company=request.user.company)
            serializer = WarningListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_warning'])
        paginate = request.query_params.get("paginate", "true")
        data = Warning.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(Q(description__icontains=search)|
            Q(warning_type__icontains = search)|
            Q(warning_to__full_name__icontains = search)|
            Q(warning_by__full_name__icontains = search)
        )

        if employee := request.query_params.get("employee"):
            data = data.filter(Q(warning_to__full_name = employee)|Q(warning_by__full_name = employee))

        if warning_type := request.query_params.get("warning_type"):
            data = data.filter(warning_type = warning_type)

        if severity := request.query_params.get("severity"):
            data = data.filter(severity = severity)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if date_from := request.query_params.get("date_from"):
            data = data.filter(warning_date__gte=date_from)

        if date_to := request.query_params.get("date_to"):
            data = data.filter(warning_date__lte=date_to)

        if paginate == "false":
            serializer = WarningListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, WarningListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_warning'])
        serializer = WarningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('warning')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_warning'])
        instance = get_object_or_404(Warning, id=id, company=request.user.company)
        serializer = WarningSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('warning')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_warning'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Warning.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Warning, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("warning"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("warning")