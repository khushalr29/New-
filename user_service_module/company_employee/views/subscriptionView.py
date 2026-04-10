from rest_framework.views import APIView
from shared.models import Subscription, UserActivityLog
from ..serializers.subscriptionSerializer import SubscriptionSerializer
from shared.utils.response.handlers import ResponseHandler
from shared.utils.common.centarlisedPermission import check_permissions
from shared.logs.decorators import log_activity
from django.shortcuts import get_object_or_404
from django.utils import timezone

class SubscriptionView(APIView):
    def get(self, request, pk=None):
        if pk:
            check_permissions(request, ['view_subscription'])
            instance = get_object_or_404(Subscription, id=pk, company=request.user.company)
            serializer = SubscriptionSerializer(instance)
            return ResponseHandler.success(serializer.data)
        
        check_permissions(request, ['list_subscription'])
        data = Subscription.objects.filter(company=request.user.company).order_by("-id")
        serializer = SubscriptionSerializer(data, many=True)
        return ResponseHandler.list_success(serializer.data)

    @log_activity(UserActivityLog.CREATE, 'Subscription')
    def post(self, request):
        check_permissions(request, ['add_subscription'])
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return ResponseHandler.create_success('Subscription')
        return ResponseHandler.create_failed(serializer.errors)
