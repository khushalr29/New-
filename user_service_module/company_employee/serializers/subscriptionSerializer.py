from rest_framework import serializers
from shared.models.core.company import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id', 'company', 'plan_type', 'amount_paid', 'plan_activation_date',
            'subscription_end_date', 'payment_mode', 'remarks', 'transaction_ref_no',
            'status'
        ]
