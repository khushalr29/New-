from rest_framework import serializer
from shared.shared.models.core.company import Plain

class PlainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plain
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
