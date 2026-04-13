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

class SubscriptionListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    plan_type_name = serializers.CharField(source='plan_type.plan_name', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'company', 'company_name', 'plan_type', 'plan_type_name',
            'amount_paid', 'plan_activation_date', 'subscription_end_date',
            'payment_mode', 'remarks', 'transaction_ref_no', 'status',
            'created_at', 'updated_at',
        ]
