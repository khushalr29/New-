from rest_framework import serializers
from shared.models.core.company import Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id',
            'plan_name',
            'plan_price_inr',
            'plan_price_usd',
            'no_of_users',
            'no_of_employees',
            'payment_duration',
            'feature',
            'description',
            'visible_to_user',
            'permissions',
        ]
