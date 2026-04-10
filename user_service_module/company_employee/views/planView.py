from rest_framework.views import APIView
from shared.models import Plan, UserActivityLog
from ..serializers.planSerializer import PlanSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

class PlanView(APIView):
    permission_classes = [AllowAny]

    @log_activity(UserActivityLog.VIEW, 'Plan')
    def get(self, request, id=None):
        if id:
            instance = get_object_or_404(Plan, id=id)
            serializer = PlanSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        data = Plan.objects.all().order_by("-id")
        serializer = PlanSerializer(data, many=True)
        return ResponseHandler.list_success(serializer.data)

    @log_activity(UserActivityLog.CREATE, 'Plan')
    def post(self, request):
        check_permissions(request, ['add_plan'])
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.create_success('Plan')
        return ResponseHandler.create_failed(serializer.errors)

    @log_activity(UserActivityLog.UPDATE, 'Plan')
    def put(self, request, id=None):
        check_permissions(request, ['change_plan'])
        instance = get_object_or_404(Plan, id=id)
        serializer = PlanSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.update_success('Plan')
        return ResponseHandler.update_failed(serializer.errors)

    @log_activity(UserActivityLog.DELETE, 'Plan')
    def delete(self, request, format=None):
        check_permissions(request, ['delete_plan'])

        ids = request.data.get('ids', [])
        if not ids:
            return ResponseHandler.no_matching_data()

        users_to_delete = Plan.objects.filter(id__in=ids, company=request.user.company)
        if not users_to_delete.exists():
            return ResponseHandler.no_matching_data()

        try:
            users_to_delete.delete()
            return ResponseHandler.delete_success('Plan')
        
        except ProtectedError as e:
            return ResponseHandler.dependency_error(
                message=ResponseMessages.protected_error("Plan")
            )