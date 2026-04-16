from django.db.models import Q
from rest_framework.views import APIView
from shared.models.hr_management import Complaint
from shared.models.core.useractivity import UserActivityLog
from ..serializers.complaintsSerializer import ComplaintsSerializer, ComplaintsListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class ComplaintsView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_complaints'])
            instance = get_object_or_404(Complaint, id=id, company=request.user.company)
            serializer = ComplaintsListSerializer(instance)
            return ResponseHandler.success(serializer.data)

        check_permissions(request, ['list_complaints'])
        paginate = request.query_params.get("paginate", "true")
        data = Complaint.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(Q(complainant__icontains=search)|
            Q(against__icontains=search)|
            Q(complaint_type__icontains=search))
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)

        if complainant := request.query_params.get("complainant"):
            data = data.filter(complainant=complainant)

        if against := request.query_params.get("against"):
            data = data.filter(against=against)

        if complaint_type := request.query_params.get("complaint_type"):
            data = data.filter(complaint_type = complaint_type)
        
        if start_date := request.query_params.get("start_date"):
            data = data.filter(complaint_date__gte=start_date)
        
        if end_date := request.query_params.get("end_date"):
            data = data.filter(complaint_date__lte=end_date)

        if paginate == "false":
            serializer = ComplaintsListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, ComplaintsListSerializer, view=self)

    def post(self, request):
        check_permissions(request, ['add_complaints'])
        serializer = ComplaintsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('complaints')
        return ResponseHandler.create_failed(serializer.errors)

    def put(self, request, id=None):
        check_permissions(request, ['change_complaints'])
        instance = get_object_or_404(Complaint, id=id, company=request.user.company)
        serializer = ComplaintsSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('complaints')
        return ResponseHandler.update_failed(serializer.errors)

    def delete(self, request):
        check_permissions(request, ['delete_complaints'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)

        queryset = Complaint.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(Complaint, ids)

        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("complaints"))

        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("complaints")