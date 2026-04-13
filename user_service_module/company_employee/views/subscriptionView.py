from shared.logs import log_activity
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from shared.utils.response import ResponseHandler
from shared.models.core.company import Subscription
from shared.models.core.useractivity import UserActivityLog
from shared.utils.common import paginate_queryset,check_permissions
from ..serializers.subscriptionSerializer import SubscriptionListSerializer

class SubscriptionView(APIView):
    def get(self, request, id=None):
        check_permissions(request, ['view_subscription'] if id else ['list_subscription'])

        if id:
            subscription = get_object_or_404(Subscription, id=id, company=request.user.company)
            serializer = SubscriptionListSerializer(subscription)
            return ResponseHandler.list_success(serializer.data)

        subscriptions = Subscription.objects.all()
        search = request.query_params.get("search")
        if search:
            subscriptions = subscriptions.filter(company__company_name__icontains=search)

        params = ['status', 'payment_mode', 'plan_type']
        for param in params:
            value = request.query_params.get(param)
            if value:
                subscriptions = subscriptions.filter(**{param: value})

        subscriptions = subscriptions.select_related("company", "plan_type").order_by('-created_at')
        return paginate_queryset(subscriptions, request, SubscriptionListSerializer, view=self)


