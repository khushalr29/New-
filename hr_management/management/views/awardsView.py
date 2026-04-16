from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Award
from shared.models.core.useractivity import UserActivityLog
from ..serializers.awardsSerializer import AwardSerializer, AwardListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

class AwardView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_award'])
            instance = get_object_or_404(Award, id=id, company=request.user.company)
            serializer = AwardListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_award'])
        paginate = request.query_params.get("paginate", "true")
        print(f"DEBUG: User={request.user.email}, Company={request.user.company}")
        data = Award.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(Q(description__icontains=search) |
            Q(employee__full_name__icontains = search) |
            Q(award_type__award_type__icontains = search)
            )
        status = request.query_params.get("status")
        
        if award_type:= request.query_params.get("award_type"):
            data = data.filter(award_type__award_type = award_type)

        if employee:= request.query_params.get("employee"):
            data = data.filter(employee__full_name = employee)

        if status:
            data = data.filter(status=status)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            try:
                start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                data = data.filter(created_at__date__gte=start, created_at__date__lte=end)
            except ValueError:
                pass
        if paginate == "false":
            serializer = AwardListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AwardListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_award'])
        serializer = AwardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('award')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_award'])
        instance = get_object_or_404(Award, id=id, company=request.user.company)
        serializer = AwardSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('award')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_award'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Award.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Award, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("award"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("award")
