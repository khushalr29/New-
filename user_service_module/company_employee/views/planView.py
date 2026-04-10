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
    def get(self, request, pk=None):
        # We allow listing and viewing plans without authentication as per AllowAny
        if pk:
            instance = get_object_or_404(Plan, id=pk)
            serializer = PlanSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        data = Plan.objects.all().order_by("-id")
        serializer = PlanSerializer(data, many=True)
        return ResponseHandler.list_success(serializer.data)

    @log_activity(UserActivityLog.CREATE, 'Plan')
    def post(self, request):
        # Creation still requires authentication/permissions
        check_permissions(request, ['add_plan'])
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.create_success('Plan')
        return ResponseHandler.create_failed(serializer.errors)
