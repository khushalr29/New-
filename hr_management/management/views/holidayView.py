from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Holiday
from shared.models.core.useractivity import UserActivityLog
from ..serializers.holidaySerializer import HolidaySerializer, HolidayListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class HolidayView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_holiday'])
            instance = get_object_or_404(Holiday, id=id, company=request.user.company)
            serializer = HolidayListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_holiday'])
        paginate = request.query_params.get("paginate", "true")
        data = Holiday.objects.filter(company=request.user.company).order_by("-id")
        
        if search := request.query_params.get("search"):
            data = data.filter(holiday_name__icontains=search)

        if status :=request.query_params.get("status"):
            data = data.filter(status=status)

        if category := request.query_params.get("category"):
            data = data.filter(category=category)

        if branch := request.query_params.get("branch"):
            data = data.filter(branch__branch_name=branch)

        if year := request.query_params.get("year"):
            data = data.filter(start_date__year=year)

        if start_date := request.query_params.get("start_date"):
            data = data.filter(start_date__gte=start_date)
        
        if end_date := request.query_params.get("end_date"):
            data = data.filter(end_date__lte=end_date)

        if paginate == "false":
            serializer = HolidayListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, HolidayListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_holiday'])
        serializer = HolidaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('holiday')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_holiday'])
        instance = get_object_or_404(Holiday, id=id, company=request.user.company)
        serializer = HolidaySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('holiday')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_holiday'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Holiday.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Holiday, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("holiday"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("holiday")