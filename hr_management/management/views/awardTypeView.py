from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import AwardType
from shared.models.core.useractivity import UserActivityLog
from ..serializers.awardTypeSerializer import AwardTypeSerializer, AwardTypeListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class AwardTypeView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_award_type'])
            instance = get_object_or_404(AwardType, id=id, company=request.user.company)
            serializer = AwardTypeListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_award_type'])
        paginate = request.query_params.get("paginate", "true")
        data = AwardType.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(award_type__icontains=search)
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
        if paginate == "false":
            serializer = AwardTypeListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AwardTypeListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_award_type'])
        serializer = AwardTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('award_type')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_award_type'])
        instance = get_object_or_404(AwardType, id=id, company=request.user.company)
        serializer = AwardTypeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('award_type')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_award_type'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = AwardType.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(AwardType, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("award_type"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("award_type")
