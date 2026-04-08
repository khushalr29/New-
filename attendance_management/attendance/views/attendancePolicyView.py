from rest_framework.views import APIView
from shared.models import AttendancePolicy, UserActivityLog
from ..serializers.attendencePolicySerializer import AttendencePolicySerializer, AttendencePolicyListSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.response.messages import ResponseMessages
from shared.utils.common.pagination import paginate_queryset
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from shared.utils.errors.protectedErrors import check_references_and_get_deletable_instances
from django.shortcuts import get_object_or_404
from django.utils import timezone

class AttendencePolicyView(APIView):
    def get(self, request, id=None):
        if id:
            check_permissions(request, ['view_attendancepolicy'])
            instance = get_object_or_404(AttendancePolicy, id=id, company=request.user.company)
            serializer = AttendencePolicyListSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_attendancepolicy'])
        paginate = request.query_params.get("paginate", "true")
        data = AttendancePolicy.objects.filter(company=request.user.company).order_by("-id")
        search = request.query_params.get("search")
        if search:
            data = data.filter(policy_name__icontains=search)
        status = request.query_params.get("status")
        if status:
            data = data.filter(status=status)
    
        if paginate == "false":
            serializer = AttendencePolicyListSerializer(data, many=True)
            return ResponseHandler.list_success(serializer.data)
        return paginate_queryset(data, request, AttendencePolicyListSerializer, view=self)

    @log_activity(UserActivityLog.CREATE, 'AttendencePolicy')
    def post(self, request):
        check_permissions(request, ['add_attendancepolicy'])
        serializer = AttendencePolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Attendence Policy')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'AttendencePolicy')
    def put(self, request, id=None):
        check_permissions(request, ['change_attendancepolicy'])
        instance = get_object_or_404(AttendancePolicy, id=id, company=request.user.company)
        serializer = AttendencePolicySerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            return ResponseHandler.update_success('Attendence Policy')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'AttendencePolicy')
    def delete(self, request):
        check_permissions(request, ['delete_attendancepolicy'])
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return ResponseHandler.bad_request(message=ResponseMessages.NO_IDS_PROVIDED)
        
        queryset = AttendancePolicy.objects.filter(id__in=ids, company=request.user.company)
        deletable_instances, reference_details = check_references_and_get_deletable_instances(AttendancePolicy, ids)
        
        if reference_details:
            return ResponseHandler.dependency_error(message=ResponseMessages.protected_error("Attendence Policy"))
        
        queryset.update(deleted_at=timezone.now())
        return ResponseHandler.delete_success("Attendence Policy")
