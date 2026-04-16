from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Announcement
from shared.models.core.useractivity import UserActivityLog
from ..serializers.announcementSerializer import    AnnouncementSerializer, AnnouncementListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

class AnnouncementView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_announcement'])
            instance = get_object_or_404(Announcement, id=id, company=request.user.company)
            serializer = AnnouncementListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_announcement'])
        paginate = request.query_params.get("paginate", "true")
        data = Announcement.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(Q(title__icontains=search) | Q(content__icontains=search))
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
        if priority:= request.query_params.get("priority"):
            data = data.filter(priority=priority)
        if category := request.query_params.get("category"):
            data = data.filter(category=category)
        if department :=request.query_params.get("department"):
            data = data.filter(department = department)
        if branch := request.query_params.get("branch"):
            data = data.filter(branch = branch)

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
            serializer = AnnouncementListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AnnouncementListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_announcement'])
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('announcement')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_announcement'])
        instance = get_object_or_404(Announcement, id=id, company=request.user.company)
        serializer = AnnouncementSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('announcement')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_announcement'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Announcement.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Announcement, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("announcement"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("announcement")
